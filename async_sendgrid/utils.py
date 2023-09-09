from __future__ import annotations
from typing import TYPE_CHECKING
from httpx import AsyncClient  # type: ignore

if TYPE_CHECKING:
    from typing import Any


def create_session(headers: dict[Any, Any]) -> AsyncClient:
    """
    create an httpx session.

    Parameters
    ----------
        headers : dict[Any, Any]

    Returns
    -------
        AsyncClient
    """
    session = AsyncClient(headers=headers)
    return session
