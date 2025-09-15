import argparse
import asyncio
import logging
import os
import subprocess

from dotenv import load_dotenv
import uvicorn


load_dotenv()


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
PORT = int(os.getenv("PORT", "3000"))
HOST = os.getenv("HOST", "127.0.0.1")


logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger("main")


def run_migrations():
    """Run database migrations using alembic."""
    try:
        logger.info("Running database migrations...")
        subprocess.run(
            ["alembic", "upgrade", "head"],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("Database migrations completed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Migration failed: {e.stderr}")
        raise


async def run_api_dev():
    logger.info("Starting API in DEV mode...")
    uvicorn.run(
        "src.main:app",
        host=HOST,
        port=PORT,
        reload=True,
    )


async def run_api():
    logger.info("Starting API...")
    server = uvicorn.Server(uvicorn.Config(
        "src.main:app",
        host=HOST,
        port=PORT,
    ))
    await server.serve()


async def run_worker():
    from src.worker import create_worker

    worker = await create_worker()
    logger.info("Starting worker...")
    await worker.run()


async def run(with_api=False, with_worker=False, dev_mode=False):
    run_migrations()

    # Dev mode is API-only
    if dev_mode:
        if not with_api:
            logger.error("Dev mode requires --api flag")
            return
        if with_worker:
            logger.error("Dev mode cannot be used with --worker")
            return
        await run_api_dev()
        return

    tasks = []

    if with_api:
        tasks.append(asyncio.create_task(run_api()))

    if with_worker:
        tasks.append(asyncio.create_task(run_worker()))

    if tasks:
        await asyncio.gather(*tasks)


def main():
    parser = argparse.ArgumentParser(description="OneRun Application")
    parser.add_argument(
        "--api",
        action="store_true",
        help="Start the API server",
    )
    parser.add_argument(
        "--worker",
        action="store_true",
        help="Start the worker",
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Enable development mode with reload (for API)",
    )

    args = parser.parse_args()

    if not args.api and not args.worker:
        parser.error("At least one of --api or --worker must be specified")

    if args.dev and not args.api:
        parser.error("--dev flag can only be used with --api")

    try:
        asyncio.run(run(
            with_api=args.api,
            with_worker=args.worker,
            dev_mode=args.dev,
        ))
    except KeyboardInterrupt:
        pass
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    main()
