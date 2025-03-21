# banjos_restaurant\app\core\config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "banjos_restaurant")

# Static files configuration
STATIC_FILES_DIR = "static"
IMAGES_DIR = os.path.join(STATIC_FILES_DIR, "images")

# Ensure the static/images directory exists
os.makedirs(IMAGES_DIR, exist_ok=True)