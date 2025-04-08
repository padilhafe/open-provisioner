from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Importa os models para que o Alembic reconheça
from .user import User
