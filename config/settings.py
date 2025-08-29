import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Example settings
SECRET_KEY = os.getenv('SECRET_KEY', 'sk-VHkpB_vIIyA1_9lWH3bt1w')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Add other settings as needed