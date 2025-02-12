import os
from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Configuration(BaseSettings):
    MONGO_URI: str = os.getenv("MONGO_URI")
    PI_EDGE_BASE_URL: str = os.getenv("PI_EDGE_BASE_URL")
    PI_EDGE_USERNAME: str = os.getenv("PI_EDGE_USERNAME")
    PI_EDGE_PASSWORD: str = os.getenv("PI_EDGE_PASSWORD")
    HTTP_PROXY: str = os.getenv("HTTP_PROXY")


config = Configuration()
