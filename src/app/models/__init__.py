from sqlalchemy.orm import declarative_base

Base = declarative_base()

import app.models.user
import app.models.device
import app.models.cpe
import app.models.customer