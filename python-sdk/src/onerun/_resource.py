from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._client import Client


class APIResource:
    _client: Client

    def __init__(self, client: Client) -> None:
        self._client = client
