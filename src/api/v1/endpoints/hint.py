"""
Define FastAPI route handlers for versioned API endpoints.

- Split routers by domain (user, training, auth, etc).
- Avoid business logic here — delegate to service/repository layers.
- Use Pydantic models for request/response.

Group endpoints inside routers and include them in the central API router.
"""

from fastapi import APIRouter
from starlette import status


class Hint:
    __router: APIRouter = APIRouter(
        prefix="/hint",
    )

    @property
    def get_router(self):
        return self.__router


    @__router.get(
        path="/ping",
        summary="Ping",
        status_code=status.HTTP_200_OK,
    )
    def ping(self) -> str:
        return "pong"


hint = Hint()