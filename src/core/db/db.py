"""
Initialize and expose database connection/session utilities.

- Create async engine and session factory.
- Provide session generator (dependency or context manager).
- Typically used by repositories and services.

Recommended: use SQLAlchemy 2.0 async-style (no ORM sync mixins).
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from src.config import cfg

async_engine = create_async_engine(
    cfg.database.async_database_url,
)
async_session_maker = async_sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine
)
Base = declarative_base()
