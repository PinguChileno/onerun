from typing import Any

from ...types import Simulation, SimulationStatus, Pagination
from ..._resource import APIResource
from .conversations import Conversations


class Simulations(APIResource):
    def __init__(self, client) -> None:
        self._client = client
        self.conversations = Conversations(client)

    def list(
        self,
        project_id: str,
        *,
        agent_id: str | None = None,
        limit: int = 10,
        name: str | None = None,
        offset: int = 0,
        sort_by: str = "created_at",
        sort_dir: str = "asc",
        status: SimulationStatus | None = None,
    ) -> Pagination[Simulation]:
        """List simulations with optional filtering and pagination."""
        url = f"{self._client.base_url}/v1/simulations"

        params: dict[str, Any] = {"project_id": project_id}

        if agent_id:
            params["agent_id"] = agent_id

        if name:
            params["name"] = name

        if status:
            params["status"] = (
                status.value
                if isinstance(status, SimulationStatus)
                else status
            )

        if sort_by != "created_at":
            params["sort_by"] = sort_by

        if sort_dir != "asc":
            params["sort_dir"] = sort_dir

        if limit != 10:
            params["limit"] = limit

        if offset != 0:
            params["offset"] = offset

        return self._client._request(
            method="GET",
            url=url,
            cast_to=Pagination[Simulation],
            params=params,
        )

    def get(
        self,
        project_id: str,
        simulation_id: str,
    ) -> Simulation:
        """Get a specific simulation by ID."""
        url = f"{self._client.base_url}/v1/simulations/{simulation_id}"

        params = {
            "project_id": project_id,
        }

        return self._client._request(
            method="GET",
            url=url,
            cast_to=Simulation,
            params=params,
        )
