import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.core.database import Base
from app.models import user 
from app.core.database import SQLALCHEMY_DATABASE_URL

# this is the Alembic Config object
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

connectable = engine_from_config(
    {
        "sqlalchemy.url": SQLALCHEMY_DATABASE_URL
    },
    prefix='sqlalchemy.',
    poolclass=pool.NullPool,
)
