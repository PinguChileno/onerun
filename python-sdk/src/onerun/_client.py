from typing import Any, cast, overload
import os

import httpx
from pydantic import BaseModel

from ._types import ResponseT
from ._version import __version__
from .resources.simulations.simulations import Simulations


class APIError(Exception):
    """Custom API error."""

    def __init__(
        self,
        code: str,
        message: str,
    ):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


class Client:
    base_url: str
    api_key: str
    timeout: int
    max_retries: int
    client: httpx.Client

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: int = 30,
        max_retries: int = 3,
        headers: dict[str, str] | None = None
    ):
        """
        Initialize the OneRun API client.

        Args:
            base_url: Base URL for the OneRun API. Defaults to the
                `ONERUN_API_BASE_URL` environment variable.
            api_key: API key for authentication. Defaults to the
                `ONERUN_API_KEY` environment variable.
            timeout: Request timeout in seconds. Default is 30 seconds.
            max_retries: Maximum number of retries for failed requests.
                Default is 3.
            headers: Optional headers to include in every request.
        """
        base_url = base_url or os.getenv("ONERUN_API_BASE_URL", "")
        base_url = base_url.rstrip("/")

        if not base_url:
            raise ValueError(
                "Base URL must be provided via argument or "
                "ONERUN_API_BASE_URL environment variable."
            )

        api_key = api_key or os.getenv("ONERUN_API_KEY", "")

        if not api_key:
            raise ValueError(
                "API key must be provided via argument or "
                "ONERUN_API_KEY environment variable."
            )

        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries

        default_headers: dict[str, str] = {
            "User-Agent": f"OneRun-Python-SDK {__version__}",
            "x-api-key": self.api_key,
        }

        if headers is not None:
            default_headers.update(headers)

        self.client = httpx.Client(
            timeout=self.timeout,
            headers=default_headers,
            limits=httpx.Limits(
                max_keepalive_connections=10,
                max_connections=20,
            ),
            transport=httpx.HTTPTransport(retries=self.max_retries)
        )

        self.simulations = Simulations(self)

    @overload
    def _request(
        self,
        method: str,
        url: str,
        cast_to: None,
        headers: dict[str, str] | None = None,
        timeout: int | None = None,
        json: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None: ...

    @overload
    def _request(
        self,
        method: str,
        url: str,
        cast_to: type[ResponseT],
        headers: dict[str, str] | None = None,
        timeout: int | None = None,
        json: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> ResponseT: ...

    def _request(
        self,
        method: str,
        url: str,
        cast_to: type[ResponseT] | None,
        headers: dict[str, str] | None = None,
        timeout: int | None = None,
        json: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> ResponseT | None:
        request_timeout: int = timeout if timeout is not None else self.timeout
        request_headers: dict[str, str] = headers or {}

        if json:
            request_headers["Content-Type"] = "application/json"

        try:
            response = self.client.request(
                method,
                url,
                headers=request_headers,
                timeout=request_timeout,
                json=json,
                **kwargs
            )
            response.raise_for_status()

            return self._process_response(response, cast_to)  # type: ignore

        except httpx.HTTPStatusError as exc:
            self._handle_http_error(exc)
            raise
        except httpx.TimeoutException as exc:
            raise APIError(
                "TIMEOUT_ERROR",
                f"Request timed out after {request_timeout}s",
            ) from exc
        except httpx.NetworkError as exc:
            raise APIError(
                "NETWORK_ERROR",
                f"Connection failed: {str(exc)}",
            ) from exc
        except httpx.RequestError as exc:
            raise APIError(
                "REQUEST_ERROR",
                f"Request failed: {str(exc)}"
            ) from exc

    def _process_response(
        self,
        response: httpx.Response,
        cast_to: type[ResponseT] | None
    ) -> ResponseT | None:
        """Process HTTP response and cast to desired type."""
        if cast_to is None:
            return None

        # Type-safe check for Pydantic models
        if isinstance(cast_to, type) and issubclass(cast_to, BaseModel):
            try:
                data = response.json()
                model = cast_to.model_validate(data)
                return cast(ResponseT, model)
            except Exception as exc:
                raise APIError(
                    "PARSE_ERROR",
                    f"Failed to parse response as {cast_to.__name__}: "
                    f"{str(exc)}"
                ) from exc

        # For other types, just return parsed JSON
        try:
            return cast(ResponseT, response.json())
        except Exception as exc:
            raise APIError(
                "PARSE_ERROR",
                f"Failed to parse JSON response: {str(exc)}"
            ) from exc

    def _handle_http_error(self, exc: httpx.HTTPStatusError) -> None:
        """Handle HTTP errors with detailed error information."""
        response = exc.response
        try:
            data = response.json()
            code = data.get("code") or "UNKNOWN"
            message = data.get("message") or data.get("detail") or str(exc)
        except Exception:
            code = "UNKNOWN"
            message = "Something went wrong"
        raise APIError(code, message) from exc
