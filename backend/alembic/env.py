import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# --- Add application directory to sys.path ---
# This allows Alembic to find your models
# Assumes alembic directory is one level down from project root where 'app' resides
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, APP_DIR)
# ---

# --- Import Base and models ---
# Import your Base metadata and all models here so Alembic autogenerate can see them
from app.database import Base # Import Base from your database setup
from app.models import user # Import all model modules
# Add imports for other models here (e.g., from app.models import project, etc.)
# ---

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# --- Use database URL from settings --- 
# Import your settings and set the sqlalchemy.url here
from app.config import settings
if settings.DATABASE_URL:
     config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
# ---

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Set target metadata --- 
# For 'autogenerate' support
target_metadata = Base.metadata
# ---

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # --- Use engine config from file --- 
    # Connectable uses configuration from alembic.ini
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    # ---

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
