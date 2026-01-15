"""Authentication middleware."""

from fastapi import Request, HTTPException, status
from typing import Callable
from core.config import get_settings

settings = get_settings()


async def verify_api_key(request: Request) -> str:
    """Verify API key from request headers."""
    api_key = request.headers.get(settings.API_KEY_HEADER)
    
    # For now, allow requests without API key in development
    if not api_key and settings.ENVIRONMENT == "development":
        return "development_key"
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )
    
    # Add your API key validation logic here
    return api_key
