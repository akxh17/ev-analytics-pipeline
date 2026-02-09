import pandas as pd
from sqlalchemy import create_engine

from src.config.settings import AMAZON_SALES_CSV, DATABASE_URL


def ingest_raw_data():
    """
    Read raw EV CSV data and load it into PostgreSQL as ev_raw table.
    """

    # Read CSV
    print("Reading CSV file...")
    df = pd.read_csv(AMAZON_SALES_CSV)
    print(f"Rows: {len(df)} | Columns: {len(df.columns)}")
    print("Columns:", list(df.columns))

    # Create DB engine
    engine = create_engine(DATABASE_URL)

    # Write to database
    print("🛢️ Writing raw data to database (amazon_sales_raw)...")
    df.to_sql("amazon_sales_raw",engine,if_exists="replace",index=False)

    print("✅ Raw ingestion completed: amazon_sales_raw")


if __name__ == "__main__":
    ingest_raw_data()
