"""
FastAPI application entrypoint.

- Initializes the app.
- Registers routers and lifespan.
- Launches middleware, exception handlers, etc.
"""

from fastapi import FastAPI
from src.lifespan import lifespan
from src.config import cfg
from src.api.v1.router import api_router  # основной router
# from src.core.middleware import setup_middlewares
# from src.core.exceptions import setup_exception_handlers

app = FastAPI(
    title="My FastAPI App",
    version="1.0.0",
    lifespan=lifespan,
)

# Register API
app.include_router(api_router, prefix="/api/v1")

# Optional: Middleware, Exceptions
# setup_middlewares(app)
# setup_exception_handlers(app)


def main():
    import uvicorn

    uvicorn.run(
        app="src:app",
        host=cfg.app.host,
        port=cfg.app.port,
        reload=cfg.app.reload,
        workers=cfg.app.workers,
    )
