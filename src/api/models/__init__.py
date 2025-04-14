from sqlalchemy.orm import declarative_base

Base = declarative_base()

import api.models.user
import api.models.device
import api.models.cpe
import api.models.customer