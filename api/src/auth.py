"""Auth middleware."""

import logging
import os

from fastapi import Depends, HTTPException, status
from fastapi.requests import Request
import jwt


API_KEY = os.getenv("AUTH_API_KEY")
JWKS_URL = os.getenv("AUTH_JWKS_URL")
JWT_ISSUER = os.getenv("AUTH_JWT_ISSUER")
JWT_AUDIENCE = os.getenv("AUTH_JWT_AUDIENCE")
JWT_ALGORITHM = os.getenv("AUTH_JWT_ALGORITHM")


logger = logging.getLogger("auth")
logger.setLevel(logging.DEBUG)


async def get_token(request: Request) -> str | None:
    """Get the OAuth2 token from the header."""
    token = request.headers.get("Authorization")
    if token is not None:
        token = token.replace("Bearer ", "")
    return token


async def get_api_key(request: Request) -> str | None:
    """Get the API key from the header."""
    key = request.headers.get("x-api-key")
    return key


async def auth_middleware(
    request: Request,
    token: str | None = Depends(get_token),
    api_key: str | None = Depends(get_api_key),
):
    """Auth middleware."""
    if request.method == "OPTIONS":
        # Allow preflight requests
        return

    if token:
        logger.debug("Authenticating with token")

        jwks_client: jwt.PyJWKClient = jwt.PyJWKClient(JWKS_URL)

        try:
            signing_key = jwks_client.get_signing_key_from_jwt(token).key

            payload: dict = jwt.decode(
                token,
                signing_key,
                algorithms=[JWT_ALGORITHM],
                audience=JWT_AUDIENCE,
                issuer=JWT_ISSUER,
            )
        except Exception as e:
            logger.debug(f"Invalid token, failed to decode: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token is not valid",
            )

        user_id = payload.get("id")

        request.state.user_id = user_id

    elif api_key:
        logger.debug("Authenticating with API key")

        if not API_KEY or API_KEY == "":
            raise Exception("Missing API key configuration")

        if api_key != API_KEY:
            logger.debug("An invalid API key was provided")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key is not valid",
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key or token is required",
        )
