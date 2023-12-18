from dotenv import load_dotenv
import os


load_dotenv()


APP_ENV = os.getenv('APP_ENV')
DATABASE_URL = os.getenv('DATABASE_URL')
