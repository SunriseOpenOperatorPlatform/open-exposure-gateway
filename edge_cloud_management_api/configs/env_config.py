from dotenv import load_dotenv
import os

load_dotenv()

PI_EDGE_BASE_URL = os.getenv("PI_EDGE_BASE_URL")
PI_EDGE_USERNAME = os.getenv("PI_EDGE_USERNAME")
PI_EDGE_PASSWORD = os.getenv("PI_EDGE_PASSWORD")
HTTP_PROXY = os.getenv("HTTP_PROXY")
