import os
from dotenv import load_dotenv


load_dotenv()


APP_ENV = os.getenv("APP_ENV")
PORT = os.getenv("PORT", 5000)
