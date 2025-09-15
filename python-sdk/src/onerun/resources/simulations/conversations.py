from typing import Any

from ..._resource import APIResource
from ...types import Response, ResponseInputMessageParams


class Responses(APIResource):
    def create(
        self,
        project_id: str,
        simulation_id: str,
        conversation_id: str,
        input: list[ResponseInputMessageParams] | None = None,
        timeout: int | None = None,
    ) -> Response:
        """Generate person's response for the given input."""
        url = (
            f"{self._client.base_url}/v1/simulations/{simulation_id}"
            f"/conversations/{conversation_id}/responses"
        )

        payload: dict[str, Any] = {"input": None}

        if input:
            payload["input"] = [i.model_dump() for i in input]

        params = {
            "project_id": project_id,
        }

        return self._client._request(
            method="POST",
            url=url,
            cast_to=Response,
            timeout=timeout,
            json=payload,
            params=params,
        )


class Conversations(APIResource):
    def __init__(self, client) -> None:
        super().__init__(client)
        self.responses = Responses(client)

    def list(
        self,
        project_id: str,
        simulation_id: str,
        *,
        status: str | None = None,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        """List conversations for a simulation."""
        url = (
            f"{self._client.base_url}/v1/simulations/{simulation_id}"
            "/conversations"
        )

        params = {
            "project_id": project_id,
        }

        if status:
            params["status"] = status

        return self._client._request(
            method="GET",
            url=url,
            cast_to=dict,
            timeout=timeout,
            params=params,
        )

    def get(
        self,
        project_id: str,
        simulation_id: str,
        conversation_id: str,
        *,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        """Get details of a specific conversation."""
        url = (
            f"{self._client.base_url}/v1/simulations/{simulation_id}"
            f"/conversations/{conversation_id}"
        )

        params = {
            "project_id": project_id,
        }

        return self._client._request(
            method="GET",
            url=url,
            cast_to=dict,
            timeout=timeout,
            params=params,
        )

    def start(
        self,
        project_id: str,
        simulation_id: str,
        conversation_id: str,
        *,
        timeout: int | None = None,
    ) -> None:
        """Mark a conversation as started."""
        url = (
            f"{self._client.base_url}/v1/simulations/{simulation_id}"
            f"/conversations/{conversation_id}/start"
        )

        params = {
            "project_id": project_id,
        }

        self._client._request(
            method="POST",
            url=url,
            cast_to=None,
            timeout=timeout,
            params=params,
        )

    def end(
        self,
        project_id: str,
        simulation_id: str,
        conversation_id: str,
        *,
        timeout: int | None = None,
    ) -> None:
        """Mark a conversation as ended."""
        url = (
            f"{self._client.base_url}/v1/simulations/{simulation_id}"
            f"/conversations/{conversation_id}/end"
        )

        params = {
            "project_id": project_id,
        }

        self._client._request(
            method="POST",
            url=url,
            cast_to=None,
            timeout=timeout,
            params=params,
        )
