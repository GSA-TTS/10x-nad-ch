import os
from .base import *


# Local development config
STORAGE_PATH = os.getenv("STORAGE_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")
QUEUE_BROKER_URL = os.getenv("QUEUE_BROKER_URL")
QUEUE_BACKEND_URL = os.getenv("QUEUE_BACKEND_URL")
