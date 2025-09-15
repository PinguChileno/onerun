# OneRun Python SDK

A Python SDK for interacting with the OneRun API to run simulations and conversations.

## Installation

```bash
uv add onerun
```

## Quick Start

```python
import onerun

# Initialize the client
client = onerun.Client(
    base_url="https://api.onerun.com",
    api_key="your-api-key"
)

# List simulations
simulations = client.simulations.list(project_id="your-project-id")

# Get a specific simulation
simulation = client.simulations.get(
    project_id="your-project-id",
    simulation_id="sim-123"
)

# List conversations in a simulation
conversations = client.simulations.conversations.list(
    project_id="your-project-id",
    simulation_id="sim-123"
)
```

## Worker Example

Create a worker to process conversations:

```python
import asyncio
import onerun
from onerun.connect import WorkerOptions, run

async def handle_conversation(context):
    """Process a conversation"""
    print(f"Processing conversation {context.conversation_id}")
    
    # Your conversation processing logic here
    await asyncio.sleep(1)  # Simulate work

# Set up worker options
options = WorkerOptions(
    project_id="your-project-id",
    agent_id="your-agent-id",
    client=onerun.Client(),
    entrypoint=handle_conversation,
    task_poll_interval=5,
    max_concurrent_tasks=10
)

# Run the worker
run(options)
```

## Configuration

The SDK can be configured using environment variables:

- `ONERUN_API_BASE_URL`: Base URL for the OneRun API
- `ONERUN_API_KEY`: Your API key for authentication
