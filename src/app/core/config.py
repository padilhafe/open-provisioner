from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "OpenProvisioner")
    ENV: str = os.getenv("ENV", "development")

settings = Settings()
