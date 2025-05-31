from fastapi import APIRouter

from .hint import hint

routers: dict[str, APIRouter] = {
    "Hint": hint.get_router(),
}

__all__ = [
    "routers",
]
