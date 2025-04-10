from dotenv import load_dotenv
import os

load_dotenv()
ENV = os.getenv("ENV", "dev")

if ENV not in ["prod", "production"]:
    load_dotenv(f".env.{ENV}", override=True)
else:
    load_dotenv(".env.prod", override=True)

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "OpenProvisioner")
    ENV: str = ENV
    DB_ENGINE: str = os.getenv("DB_ENGINE", "postgresql")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")

    # Assíncrona para o app
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Síncrona para o Alembic
    SYNC_DATABASE_URL: str = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

settings = Settings()
