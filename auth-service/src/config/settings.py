import os

from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DB_URL')
PRIVATE_PATH = os.getenv('SECRET_KEY_FILE')
ALGORITHM = os.getenv('ALGORITHM')

with open(PRIVATE_PATH, 'r') as file:
    PRIVATE_KEY = file.read()
