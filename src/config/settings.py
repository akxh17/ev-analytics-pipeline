import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# -------------------------------
# Database Configuration
# -------------------------------
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# SQLAlchemy database URL
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# -------------------------------
# File Paths
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_RAW = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED = os.path.join(BASE_DIR, "data", "processed")

# Example CSV path
AMAZON_SALES_CSV = os.path.join(DATA_RAW, "amazon_sales_dataset.csv")