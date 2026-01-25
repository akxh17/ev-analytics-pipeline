import pandas as pd
from sqlalchemy import create_engine

from src.config.settings import EV_CSV, DATABASE_URL


def ingest_raw_data():
    """
    Read raw EV CSV data and load it into PostgreSQL as ev_raw table.
    """

    # Read CSV
    print("Reading CSV file...")
    df = pd.read_csv(EV_CSV)
    print(f"Raw data shape: {df.shape}")

    # Create DB engine
    engine = create_engine(DATABASE_URL)

    # Write to database
    print("Writing raw data to database (table: ev_raw)...")
    df.to_sql(
        "ev_raw",
        engine,
        if_exists="replace",
        index=False
    )

    print("✅ Raw table written successfully: ev_raw")


if __name__ == "__main__":
    ingest_raw_data()
