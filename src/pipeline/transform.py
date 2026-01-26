import pandas as pd
from sqlalchemy import create_engine
from src.config.settings import DATABASE_URL

def transform_raw_to_staging():
    print("Reading raw data from database...")
    
    engine = create_engine(DATABASE_URL)
    
    df = pd.read_sql("SELECT * FROM ev_raw", engine)
    print(f"Raw rows: {len(df)}")

    # -------------------------------
    # Standardize column names
    # -------------------------------
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w]", "", regex=True)
    )

    # -------------------------------
    # Drop duplicates
    # -------------------------------
    df.drop_duplicates(inplace=True)

    # -------------------------------
    # Type conversions (safe ones)
    # -------------------------------
    if "model_year" in df.columns:
        df["model_year"] = pd.to_numeric(df["model_year"], errors="coerce")

    if "electric_range" in df.columns:
        df["electric_range"] = pd.to_numeric(df["electric_range"], errors="coerce")

    print(f"Staging rows after cleanup: {len(df)}")

    # -------------------------------
    # Write to staging table
    # -------------------------------
    print("Writing cleaned data to staging table (ev_staging)...")
    df.to_sql(
        "ev_staging",
        engine,
        if_exists="replace",
        index=False
    )

    print("✅ Data successfully written to ev_staging")

if __name__ == "__main__":
    transform_raw_to_staging()
