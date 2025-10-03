import os
import re
from logging.config import fileConfig

from alembic import context
from alembic.script import write_hooks
from maximus.database.schemas import metadata
from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

compare_server_default = lambda *_args, **_kwargs: None  # noqa: E731

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    config.set_main_option('sqlalchemy.url', DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

ADD_COLUMN_REGEX = re.compile(
    r'op\.add_column\([\'"]([^\'"]+)[\'"], sa\.Column\([\'"]([^\'"]+)[\'"].*nullable=False'
)


@write_hooks.register('columns_non_nullable_fields')
def fix_columns_non_nullable_fields(filename, options):  # noqa: ARG001
    with open(filename) as f:
        lines = f.readlines()

    # Convert
    i = 0
    while i < len(lines):
        res = ADD_COLUMN_REGEX.search(lines[i])
        if not res:
            i += 1
            continue

        table_name, column_name = res.groups()
        lines[i] = lines[i].replace('nullable=False', 'nullable=True')
        lines.insert(
            i + 1,
            f"    op.execute('UPDATE {table_name} SET {column_name} = 0')  # TODO: update with default value\n",
        )
        lines.insert(
            i + 2,
            f"    op.alter_column('{table_name}', '{column_name}', nullable=False)\n",
        )
        i += 2

    with open(filename, 'w') as f:
        f.write(''.join(lines))


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        compare_server_default=compare_server_default,
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            compare_server_default=compare_server_default,
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
