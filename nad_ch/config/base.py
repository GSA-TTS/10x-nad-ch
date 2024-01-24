import os
from dotenv import load_dotenv


load_dotenv()


APP_ENV = os.getenv("APP_ENV")
WEB_PORT = os.getenv("WEB_PORT", 3000)
