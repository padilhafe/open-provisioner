import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Ajusta o sys.path para conseguir importar o app corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# Importa configurações do projeto
from app.core.config import Settings

# Define URL do banco para o Alembic
config = context.config
config.set_main_option("sqlalchemy.url", Settings.DATABASE_URL)

# Configura logging
fileConfig(config.config_file_name)

# Importa os modelos (todos que devem ser refletidos no banco)
from app.models import Base
from app.models import user, device, customer, cpe

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Executa as migrações em modo offline (sem conectar no banco)."""
    context.configure(
        url=Settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Executa as migrações conectando ao banco."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

# Decide se roda online ou offline
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
