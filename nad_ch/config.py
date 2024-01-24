from dotenv import load_dotenv
import json
import os


def get_credentials(service_name, default={}):
    service = vcap_services.get(service_name, [default])
    return service[0].get("credentials", default) if service else default


load_dotenv()


vcap_services = json.loads(os.getenv("VCAP_SERVICES", "{}"))


postgres_credentials = get_credentials("aws-rds")
redis_credentials = get_credentials("aws-elasticache-redis")
s3_credentials = get_credentials("s3")


APP_ENV = os.getenv("APP_ENV")
WEB_PORT = os.getenv("WEB_PORT")

# Remote development config
DATABASE_URL = postgres_credentials.get("uri", os.getenv("DATABASE_URL"))
QUEUE_HOST = redis_credentials.get("hostname", os.getenv("QUEUE_HOST"))
QUEUE_PORT = redis_credentials.get("port", os.getenv("QUEUE_PORT"))
QUEUE_PASSWORD = redis_credentials.get("password", os.getenv("QUEUE_PASSWORD"))
S3_BUCKET_NAME = s3_credentials.get("bucket", os.getenv("S3_BUCKET_NAME"))
S3_ENDPOINT = s3_credentials.get("endpoint", os.getenv("S3_ENDPOINT"))
S3_ACCESS_KEY = s3_credentials.get("access_key_id", os.getenv("S3_ACCESS_KEY"))
S3_SECRET_ACCESS_KEY = s3_credentials.get(
    "secret_access_key", os.getenv("S3_SECRET_ACCESS_KEY")
)
S3_REGION = s3_credentials.get("region", os.getenv("S3_REGION"))

# Local development config
STORAGE_PATH = os.getenv("STORAGE_PATH")
DATABASE_URL_LOCAL = os.getenv("DATABASE_URL_LOCAL")
QUEUE_BROKER_URL_LOCAL = os.getenv("QUEUE_BROKER_URL_LOCAL")
QUEUE_BACKEND_URL_LOCAL = os.getenv("QUEUE_BACKEND_URL_LOCAL")
