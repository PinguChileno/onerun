import asyncio
import logging
import signal
import sys
import time
import traceback
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Awaitable, Callable, Optional
from apscheduler import AsyncScheduler
from apscheduler.triggers.interval import IntervalTrigger
import uvicorn
from fastapi import FastAPI

from onerun.types.simulations import SimulationStatus

from .._client import Client
from .types import RunConversationContext


logger = logging.getLogger("onerun.worker")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

queued_run_tasks = {}  # conversation_id -> conversation dict
processing_run_tasks = set()  # conversation_ids being processed


class ShutdownManager:
    """Manages graceful shutdown of the worker"""

    def __init__(self):
        self._shutdown_requested = False
        self._active_jobs = set()

    def request_shutdown(self):
        self._shutdown_requested = True

    def is_shutdown_requested(self) -> bool:
        return self._shutdown_requested

    def register_active_job(self, job_id: str):
        self._active_jobs.add(job_id)

    def unregister_active_job(self, job_id: str):
        self._active_jobs.discard(job_id)

    def has_active_jobs(self) -> bool:
        return len(self._active_jobs) > 0


# Global shutdown manager
shutdown_manager = ShutdownManager()


@dataclass
class WorkerOptions:
    """Configuration for the worker"""

    # Project and agent identifiers
    project_id: str
    """ID of the project to work on"""
    agent_id: str
    """ID of the agent to use for conversations"""

    # API connection
    client: Client
    """OneRun API client instance"""

    # Entrypoint function to run for each conversation
    entrypoint: Callable[[RunConversationContext], Awaitable[None]]
    """Async function to execute for each conversation"""

    # Task processing settings
    task_poll_interval: int = 5
    """Interval in seconds to poll for new tasks"""
    max_concurrent_tasks: int = 10
    """Maximum number of concurrent tasks to process"""

    # Server settings (for metrics/status)
    server_host: str = "0.0.0.0"
    """Host for the server"""
    server_port: int = 8000
    """Port for the server"""


class Worker:
    """Main worker for processing conversation tasks"""

    project_id: str
    agent_id: str

    client: Client

    max_concurrent_tasks: int
    task_poll_interval: int

    def __init__(self, options: WorkerOptions) -> None:
        self.project_id = options.project_id
        self.agent_id = options.agent_id
        self.client = options.client
        self.entrypoint = options.entrypoint
        self.task_poll_interval = options.task_poll_interval
        self.max_concurrent_tasks = options.max_concurrent_tasks

        self.running = False
        self.semaphore = asyncio.Semaphore(options.max_concurrent_tasks)

    async def poll_run_tasks(self) -> None:
        """Poll for available conversation tasks"""
        if shutdown_manager.is_shutdown_requested():
            return

        job_id = "poll_run_tasks"
        shutdown_manager.register_active_job(job_id)

        try:
            logger.info("Polling for queued conversations...")

            try:
                try:
                    response = self.client.simulations.list(
                        project_id=self.project_id,
                        agent_id=self.agent_id,
                        status=SimulationStatus.IN_PROGRESS,
                        limit=10,
                    )
                    simulations = response.data
                except Exception as e:
                    logger.error(
                        f"Error fetching simulations via API client: {e}"
                    )
                    raise

                logger.info(
                    f"Found {len(simulations)} in-progress simulations"
                )

                total_processed_count = 0

                # For each simulation, get queued conversations
                for simulation in simulations:
                    if shutdown_manager.is_shutdown_requested():
                        break

                    simulation_id = simulation.id
                    logger.info(
                        f"Fetching conversations for simulation "
                        f"{simulation_id}"
                    )

                    try:
                        response = self.client.simulations.conversations.list(
                            project_id=self.project_id,
                            simulation_id=simulation_id,
                            status="queued",
                        )
                        conversations = response.get("data", [])
                    except Exception as e:
                        logger.error(
                            f"Error fetching conversations for simulation "
                            f"{simulation_id}: {e}"
                        )
                        continue

                    logger.info(
                        f"Found {len(conversations)} queued conversations for "
                        f"simulation {simulation_id}"
                    )

                    for conversation in conversations:
                        # Check for shutdown signal
                        if shutdown_manager.is_shutdown_requested():
                            break

                        conversation_id = conversation["id"]

                        if (
                            conversation_id not in queued_run_tasks
                            and conversation_id not in processing_run_tasks
                        ):
                            try:
                                # Check if we can acquire semaphore
                                if self.semaphore.locked():
                                    logger.info(
                                        "Max concurrent tasks reached, "
                                        "skipping remaining conversations"
                                    )
                                    break

                                # Queue conversation for run
                                queued_run_tasks[conversation_id] = conversation
                                total_processed_count += 1

                            except Exception as e:
                                if shutdown_manager.is_shutdown_requested():
                                    logger.debug(f"Error during shutdown: {e}")
                                    return
                                else:
                                    logger.error(
                                        f"Error queueing conversation "
                                        f"{conversation_id}: {e}"
                                    )

                if total_processed_count > 0:
                    logger.info(
                        f"Queued {total_processed_count} conversations for "
                        "run"
                    )

            except Exception as e:
                if shutdown_manager.is_shutdown_requested():
                    logger.debug(f"API error during shutdown: {e}")
                else:
                    logger.error(f"Error polling for tasks: {e}")

        except Exception as e:
            if shutdown_manager.is_shutdown_requested():
                logger.debug(f"Error during shutdown: {e}")
            else:
                logger.error(f"Unexpected error in poll_for_tasks: {e}")
                logger.error(traceback.format_exc())
        finally:
            shutdown_manager.unregister_active_job(job_id)

    async def process_run_tasks(self) -> None:
        """Process queued run tasks"""
        if shutdown_manager.is_shutdown_requested():
            return

        if not queued_run_tasks:
            return

        job_id = "process_run_tasks"
        shutdown_manager.register_active_job(job_id)

        try:
            # Process tasks up to semaphore limit
            tasks_to_process = []

            for conversation_id, conversation in list(queued_run_tasks.items()):
                if shutdown_manager.is_shutdown_requested():
                    break

                if conversation_id not in processing_run_tasks:
                    if self.semaphore.locked():
                        break

                    tasks_to_process.append((conversation_id, conversation))

            if tasks_to_process:
                logger.info(f"Processing {len(tasks_to_process)} run tasks")

                for conversation_id, conversation in tasks_to_process:
                    asyncio.create_task(self._process_run_task(conversation))

        except Exception as e:
            if shutdown_manager.is_shutdown_requested():
                logger.debug(f"Error during shutdown: {e}")
            else:
                logger.error(f"Error in process_run_tasks: {e}")
        finally:
            shutdown_manager.unregister_active_job(job_id)

    async def _process_run_task(self, conversation: dict) -> None:
        """Process a single run task for a conversation"""
        conversation_id = conversation["id"]
        simulation_id = conversation["simulation_id"]

        async with self.semaphore:
            processing_run_tasks.add(conversation_id)

            try:
                logger.info(
                    f"Processing conversation {conversation_id} in simulation "
                    f"{simulation_id}"
                )

                self.client.simulations.conversations.start(
                    project_id=self.project_id,
                    simulation_id=simulation_id,
                    conversation_id=conversation_id,
                )

                # Execute agent's entrypoint function
                context = RunConversationContext(
                    project_id=self.project_id,
                    simulation_id=simulation_id,
                    conversation_id=conversation_id,
                )

                await self.entrypoint(context)

                self.client.simulations.conversations.end(
                    project_id=self.project_id,
                    simulation_id=simulation_id,
                    conversation_id=conversation_id,
                )

                logger.info(f"Completed run task for {conversation_id}")

            except Exception as e:
                logger.error(f"Failed run task for {conversation_id}: {e}")
                logger.error(traceback.format_exc())
            finally:
                processing_run_tasks.discard(conversation_id)
                queued_run_tasks.pop(conversation_id, None)


# Global worker instance
worker: Optional[Worker] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the lifecycle of the FastAPI app with APScheduler"""
    global worker

    if not worker:
        raise RuntimeError("Worker not initialized")

    async with AsyncScheduler() as scheduler:
        # Add scheduled jobs
        await scheduler.add_schedule(
            worker.poll_run_tasks,
            IntervalTrigger(seconds=worker.task_poll_interval)
        )
        await scheduler.add_schedule(
            worker.process_run_tasks,
            IntervalTrigger(seconds=worker.task_poll_interval)
        )

        await scheduler.start_in_background()
        logger.info("Scheduler started")

        yield

        # Graceful shutdown
        logger.info("Shutting down scheduler...")
        shutdown_manager.request_shutdown()

        # Wait for active jobs to complete (with timeout)
        timeout = 10
        start_time = time.time()

        while (
            shutdown_manager.has_active_jobs() and
            (time.time() - start_time) < timeout
        ):
            await asyncio.sleep(0.1)

        await scheduler.stop()
        await scheduler.wait_until_stopped()
        logger.info("Scheduler stopped")


def create_app() -> FastAPI:
    """Create the FastAPI application for worker metrics and status"""
    app = FastAPI(lifespan=lifespan)

    @app.get("/health")
    def health():
        return {"status": "healthy"}

    @app.get("/metrics")
    def metrics():
        processing_tasks = len(processing_run_tasks)
        queued_tasks = len(queued_run_tasks)
        max_concurrent_tasks = worker.max_concurrent_tasks if worker else 0
        poll_interval = worker.task_poll_interval if worker else 0

        return {
            "processing_tasks": processing_tasks,
            "queued_tasks": queued_tasks,
            "max_concurrent_tasks": max_concurrent_tasks,
            "poll_interval": poll_interval,
        }

    return app


def signal_handler(signum: int, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}, requesting shutdown...")
    shutdown_manager.request_shutdown()


def run(options: WorkerOptions) -> None:
    """Run the worker"""
    global worker

    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    worker = Worker(options)

    app = create_app()

    logger.info(
        f"Starting app on: {options.server_host}:{options.server_port}"
    )

    logger.info(f"Task polling interval: {options.task_poll_interval}s")

    try:
        uvicorn.run(
            app,
            host=options.server_host,
            port=options.server_port,
            log_level="warning"  # Reduce uvicorn noise
        )
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

    logger.info("Worker shutdown complete")
