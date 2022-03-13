#!/usr/bin/env python3
"""Create the database based on the current Model definition, ignoring any and all migrations"""
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine

from movements.database import BaseMeta
from movements.settings import PROJECT_ROOT, settings

engine = create_engine(settings.DATABASE_URL)

BaseMeta.metadata.create_all(engine)

# Load the Alembic configuration and generate the
# version table, "stamping" it with the most recent rev:
config_path = str(PROJECT_ROOT / 'alembic.ini')
alembic_cfg = Config(config_path)
command.stamp(alembic_cfg, 'head')

# To prune old migration files, simply delete the files.
# Then, in the earliest, still-remaining migration file,
# set `down_revision`=None
