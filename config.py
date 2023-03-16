import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
