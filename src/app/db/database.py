# app/db/database.py

import os
from databases import Database
from app.core.config import Settings

database = Database(Settings.DATABASE_URL)
