# api/db/database.py

import os
from databases import Database
from api.core.config import Settings

database = Database(Settings.DATABASE_URL)
