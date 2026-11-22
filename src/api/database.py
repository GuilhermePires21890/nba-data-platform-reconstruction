import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

password = os.getenv("POSTGRES_PASSWORD")
if not password:
    raise RuntimeError("POSTGRES_PASSWORD is required")

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "dbname": os.getenv("POSTGRES_DB", "nba_data_platform"),
    "user": os.getenv("POSTGRES_USER", "nba_admin"),
    "password": password,
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)