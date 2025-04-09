# src/app/core/settings.py
from dotenv import load_dotenv
import os

# Load an initial .env to get ENV, then load the specific .env.<ENV> file
load_dotenv()
ENV = os.getenv("ENV", "dev")  # Default to 'development' if ENV not set

# Load the environment-specific .env file
if ENV not in ["prod", "production"]:
    load_dotenv(f".env.{ENV}", override=True)
else:
    load_dotenv(".env.prod", override=True)

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "OpenProvisioner")
    ENV: str = ENV
    DB_ENGINE: str = os.getenv("DB_ENGINE", "mariadb")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")

    # Construct DATABASE_URL
    DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

settings = Settings()