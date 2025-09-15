import os

from temporalio.client import Client


TEMPORAL_ADDRESS = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
TEMPORAL_NAMESPACE = os.getenv("TEMPORAL_NAMESPACE", "default")

# Global client instance
_temporal_client: Client | None = None


async def init_temporal_client():
    """Initialize Temporal client on app startup."""
    global _temporal_client

    _temporal_client = await Client.connect(
        target_host=TEMPORAL_ADDRESS,
        namespace=TEMPORAL_NAMESPACE,
    )


async def close_temporal_client():
    """Close Temporal client on app shutdown."""
    global _temporal_client

    # Temporal client doesn't require explicit closing
    # Just clear the reference
    _temporal_client = None


def get_temporal_client() -> Client:
    """Get the global Temporal client instance."""
    if _temporal_client is None:
        raise RuntimeError(
            "Temporal client not initialized. "
            "Call init_temporal_client() first."
        )
    return _temporal_client
