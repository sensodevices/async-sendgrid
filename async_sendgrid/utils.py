from typing import Any
from httpx import AsyncClient


def create_session(headers: dict[Any, Any]) -> AsyncClient:
    session = AsyncClient(headers=headers)
    return session
