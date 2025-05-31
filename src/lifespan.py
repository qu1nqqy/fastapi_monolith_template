"""
Application lifecycle management.

- Define startup and shutdown events here.
- Initialize resources (DB connections, Redis, S3, etc).
- Clean up connections gracefully on shutdown.

Use with FastAPI's `lifespan` argument to hook into app lifecycle.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.core.logger import configure_logger, get_logger
# from src.core.db import init_db_connection
# from src.repository.s3.s3 import init_s3_client
# from src.core.redis import init_redis, close_redis  # если будешь юзать Redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Init logger
    configure_logger()
    logger = get_logger()
    logger.info("App startup: initializing resources")

    # Example: init_db_connection()
    # Example: await init_redis()
    # Example: await init_s3_client()

    yield  # <- здесь приложение начинает работать

    logger.info("App shutdown: releasing resources")

    # Example: await close_redis()
