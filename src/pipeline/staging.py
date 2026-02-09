import pandas as pd
from sqlalchemy import create_engine

from src.config.settings import DATABASE_URL
from src.validation.rules import AmazonSalesRules


def stage_amazon_sales():
    print("📥 Reading raw data from amazon_sales_raw...")

    engine = create_engine(DATABASE_URL)
    df = pd.read_sql("SELECT * FROM amazon_sales_raw", engine)

    raw_rows = len(df)
    print(f"Raw rows: {raw_rows}")

    # -------------------------
    # Column rename (schema alignment)
    # -------------------------
    COLUMN_RENAME_MAP = {
        "discount_percent": "discount_percentage"
    }

    df.rename(columns=COLUMN_RENAME_MAP, inplace=True)

    # Instantiate rules object
    rules = AmazonSalesRules()

    # -------------------------
    # Primary key validation
    # -------------------------
    df = df.dropna(subset=["order_id"])
    df = df.drop_duplicates(subset=["order_id"])

    # -------------------------
    # Categorical validations
    # -------------------------
    df = df[df["product_category"].isin(rules.product_categories)]
    df = df[df["customer_region"].isin(rules.customer_regions)]
    df = df[df["payment_method"].isin(rules.payment_methods)]

    # -------------------------
    # Numeric rule enforcement
    # -------------------------
    for col, rule in rules.numeric_rules.items():
        df[col] = pd.to_numeric(df[col], errors="coerce")

        if "default" in rule:
            df[col] = df[col].fillna(rule["default"])

        if "min" in rule:
            df = df[df[col] >= rule["min"]]

        if "max" in rule:
            df = df[df[col] <= rule["max"]]

    # -------------------------
    # Date parsing
    # -------------------------
    df["order_date"] = pd.to_datetime(
        df["order_date"], format="%d-%m-%Y", errors="coerce"
    )
    df = df.dropna(subset=["order_date"])

    # -------------------------
    # Final stats
    # -------------------------
    clean_rows = len(df)
    print(f"✅ Rows after staging: {clean_rows}")
    print(f"🧹 Dropped rows: {raw_rows - clean_rows}")

    # -------------------------
    # Write staging table
    # -------------------------
    print("🛢️ Writing to amazon_sales_staging...")
    df.to_sql(
        "amazon_sales_staging",
        engine,
        if_exists="replace",
        index=False,
    )

    print("🎉 Staging completed successfully")


if __name__ == "__main__":
    stage_amazon_sales()
