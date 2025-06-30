from fastapi import HTTPException, Request
from starlette.status import HTTP_403_FORBIDDEN

from app.config.config import settings


async def validate_token(request: Request) -> bool:
    """Validate the API token from the request header."""
    api_token = request.headers.get("Authorization")

    if not api_token:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Missing API token",
        )

    if api_token != f"Bearer {settings.API_TOKEN}":
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Invalid API token",
        )

    return True
