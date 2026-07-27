import asyncio
import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context


# Add project root to Python path
sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)


from app.config.settings import settings
from app.shared.database.base import Base

# Import all models so Alembic can detect them
from app.auth.models import *  # noqa: F401


# Alembic Config object
config = context.config


# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Metadata for autogenerate
target_metadata = Base.metadata


# Use database URL from Pydantic settings
# Escape % because ConfigParser uses % for interpolation
config.set_main_option(
    "sqlalchemy.url",
    settings.database_url.replace("%", "%%"),
)


def run_migrations_offline() -> None:
    """
    Run migrations without DB connection.
    """

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """
    Execute migrations with an active connection.
    """

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Create async engine and run migrations.
    """

    section = config.get_section(config.config_ini_section)

    if section is None:
        raise RuntimeError("Alembic configuration section is missing.")

    connectable = async_engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )

    async with connectable.connect() as connection:
        await connection.run_sync(
            do_run_migrations
        )

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Run migrations online.
    """

    asyncio.run(
        run_async_migrations()
    )


if context.is_offline_mode():
    run_migrations_offline()

else:
    run_migrations_online()