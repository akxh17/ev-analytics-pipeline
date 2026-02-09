import pandas as pd
from sqlalchemy import create_engine

from src.config.settings import DATABASE_URL


def transform_amazon_sales():
    print("📊 Starting transformation phase...")

    engine = create_engine(DATABASE_URL)

    # -------------------------
    # Load staging data
    # -------------------------
    df = pd.read_sql("SELECT * FROM amazon_sales_staging", engine)
    print(f"Rows loaded from staging: {len(df)}")

    # =====================================================
    # 1️⃣ Total Revenue Over Time (Daily)
    # =====================================================
    revenue_over_time = (
        df.groupby("order_date", as_index=False)
        .agg(total_revenue=("total_revenue", "sum"))
        .sort_values("order_date")
    )

    revenue_over_time.to_sql(
        "amazon_kpi_revenue_over_time",
        engine,
        if_exists="replace",
        index=False,
    )

    print("✅ Created amazon_kpi_revenue_over_time")

    # =====================================================
    # 2️⃣ Revenue by Product Category
    # =====================================================
    revenue_by_category = (
        df.groupby("product_category", as_index=False)
        .agg(
            total_revenue=("total_revenue", "sum"),
            total_quantity=("quantity_sold", "sum"),
            avg_rating=("rating", "mean"),
        )
        .sort_values("total_revenue", ascending=False)
    )

    revenue_by_category.to_sql(
        "amazon_kpi_revenue_by_category",
        engine,
        if_exists="replace",
        index=False,
    )

    print("✅ Created amazon_kpi_revenue_by_category")

    # =====================================================
    # 3️⃣ Top Products by Revenue
    # =====================================================
    top_products = (
        df.groupby("product_id", as_index=False)
        .agg(
            total_revenue=("total_revenue", "sum"),
            total_quantity=("quantity_sold", "sum"),
            avg_rating=("rating", "mean"),
        )
        .sort_values("total_revenue", ascending=False)
        .head(10)
    )

    top_products.to_sql(
        "amazon_kpi_top_products",
        engine,
        if_exists="replace",
        index=False,
    )

    print("✅ Created amazon_kpi_top_products")

    # =====================================================
    # 4️⃣ Quantity Sold by Product Category
    # =====================================================
    quantity_by_category = (
        df.groupby("product_category", as_index=False)
        .agg(
            total_quantity=("quantity_sold", "sum"),
            total_revenue=("total_revenue", "sum"),
        )
        .sort_values("total_quantity", ascending=False)
    )

    quantity_by_category.to_sql(
        "amazon_kpi_quantity_by_category",
        engine,
        if_exists="replace",
        index=False,
    )

    print("✅ Created amazon_kpi_quantity_by_category")

    # =====================================================
    # 5️⃣ Average Discount by Product Category
    # =====================================================
    avg_discount_by_category = (
        df.groupby("product_category", as_index=False)
        .agg(
            avg_discount_percent=("discount_percentage", "mean"),
            avg_original_price=("price", "mean"),
            avg_discounted_price=("discounted_price", "mean"),
        )
        .sort_values("avg_discount_percent", ascending=False)
    )

    avg_discount_by_category.to_sql(
        "amazon_kpi_avg_discount_by_category",
        engine,
        if_exists="replace",
        index=False,
    )

    print("✅ Created amazon_kpi_avg_discount_by_category")

    # =====================================================
    # 6️⃣ Discount vs Quantity Sold
    # =====================================================
    df["discount_bucket"] = pd.cut(
        df["discount_percentage"],
        bins=[-1, 10, 20, 30, 100],
        labels=["0-10%", "11-20%", "21-30%", "30%+"],
    )

    discount_impact = (
        df.groupby("discount_bucket", as_index=False)
        .agg(
            total_quantity=("quantity_sold", "sum"),
            total_revenue=("total_revenue", "sum"),
            avg_rating=("rating", "mean"),
        )
        .sort_values("discount_bucket")
    )

    discount_impact.to_sql(
        "amazon_kpi_discount_impact",
        engine,
        if_exists="replace",
        index=False,
    )

    print("✅ Created amazon_kpi_discount_impact")



    print("🎉 Transformation phase completed successfully")


if __name__ == "__main__":
    transform_amazon_sales()
