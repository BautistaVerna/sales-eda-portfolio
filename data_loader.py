"""
data_loader.py
Loads and merges the 9 Olist CSVs into a single master DataFrame.
"""

from pathlib import Path
import pandas as pd


# ── File manifest ──────────────────────────────────────────────────────────────
_CSV_FILES = {
    "orders":       "olist_orders_dataset.csv",
    "order_items":  "olist_order_items_dataset.csv",
    "products":     "olist_products_dataset.csv",
    "translations": "product_category_name_translation.csv",
    "customers":    "olist_customers_dataset.csv",
    "reviews":      "olist_order_reviews_dataset.csv",
    "payments":     "olist_order_payments_dataset.csv",
    "sellers":      "olist_sellers_dataset.csv",
    "geolocation":  "olist_geolocation_dataset.csv",
}

_DATE_COLS = {
    "orders": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "reviews": ["review_creation_date", "review_answer_timestamp"],
}


def _load_csvs(raw_path: Path) -> dict[str, pd.DataFrame]:
    """Read every CSV and parse date columns up front."""
    dfs = {}
    for key, filename in _CSV_FILES.items():
        filepath = raw_path / filename
        parse_dates = _DATE_COLS.get(key)
        dfs[key] = pd.read_csv(filepath, parse_dates=parse_dates, low_memory=False)
    return dfs


def _merge(dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Build the master DataFrame by joining all tables.

    Join strategy (all LEFT so we keep every order):
      orders → order_items   (one order → many items)
      → products             (item → product details)
      → translations         (Portuguese category → English)
      → customers            (order → customer location)
      → reviews              (order → satisfaction score)
      → payments             (order → payment summary)
      → sellers              (item → seller location)
    Geolocation is excluded from the flat merge; its granularity (zip prefix)
    is better used in the geographic section via a dedicated join.
    """
    df = (
        dfs["orders"]
        .merge(dfs["order_items"],  on="order_id",    how="left")
        .merge(dfs["products"],     on="product_id",  how="left")
        .merge(dfs["translations"], on="product_category_name", how="left")
        .merge(dfs["customers"],    on="customer_id", how="left")
    )

    # Reviews: keep one row per order (take the first review if duplicates)
    reviews_dedup = (
        dfs["reviews"]
        .sort_values("review_creation_date")
        .drop_duplicates(subset="order_id", keep="first")
        [["order_id", "review_score", "review_creation_date"]]
    )
    df = df.merge(reviews_dedup, on="order_id", how="left")

    # Payments: aggregate to one row per order (sum value, most common type)
    payments_agg = (
        dfs["payments"]
        .groupby("order_id", as_index=False)
        .agg(
            payment_value=("payment_value", "sum"),
            payment_type=("payment_type", lambda x: x.value_counts().index[0]),
            payment_installments=("payment_installments", "max"),
        )
    )
    df = df.merge(payments_agg, on="order_id", how="left")

    # Sellers: bring state/city of the seller
    df = df.merge(
        dfs["sellers"][["seller_id", "seller_state", "seller_city"]],
        on="seller_id",
        how="left",
    )

    return df


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply lightweight, non-destructive cleaning:
    - Rename the translated category column for clarity.
    - Cast low-cardinality string columns to category dtype (memory efficiency).
    - Derive commonly-needed date parts so notebooks don't repeat this logic.
    - Drop rows where order_purchase_timestamp is null (can't analyze without it).
    """
    df = df.rename(columns={"product_category_name_english": "category"})

    # Drop orders with no purchase date
    df = df.dropna(subset=["order_purchase_timestamp"])

    # Derived time columns (all from purchase timestamp)
    ts = df["order_purchase_timestamp"]
    df["order_year"]        = ts.dt.year.astype("Int16")
    df["order_month"]       = ts.dt.month.astype("Int8")
    df["order_day_of_week"] = ts.dt.dayofweek.astype("Int8")   # 0=Mon, 6=Sun
    df["order_hour"]        = ts.dt.hour.astype("Int8")
    df["year_month"]        = ts.dt.to_period("M")             # convenient for groupby

    # Delivery metrics (in days)
    df["delivery_days_actual"] = (
        (df["order_delivered_customer_date"] - df["order_purchase_timestamp"])
        .dt.days
    )
    df["delivery_days_estimated"] = (
        (df["order_estimated_delivery_date"] - df["order_purchase_timestamp"])
        .dt.days
    )
    df["delivery_delay"] = df["delivery_days_actual"] - df["delivery_days_estimated"]
    df["delivered_on_time"] = df["delivery_delay"] <= 0

    # Category dtype for memory efficiency
    for col in ["order_status", "customer_state", "seller_state",
                "payment_type", "category"]:
        if col in df.columns:
            df[col] = df[col].astype("category")

    return df.reset_index(drop=True)


def load_data(raw_path: str | Path = "data/raw") -> pd.DataFrame:
    """
    Public entry point.

    Parameters
    ----------
    raw_path : str or Path
        Directory containing the 9 Olist CSV files.

    Returns
    -------
    pd.DataFrame
        Master DataFrame, one row per order item, fully merged and cleaned.
    """
    raw_path = Path(raw_path)
    if not raw_path.exists():
        raise FileNotFoundError(f"raw_path does not exist: {raw_path.resolve()}")

    print("Loading CSVs...")
    dfs = _load_csvs(raw_path)
    for key, df in dfs.items():
        print(f"  {key:15s} → {df.shape[0]:>7,} rows × {df.shape[1]} cols")

    print("\nMerging tables...")
    df = _merge(dfs)

    print("Cleaning...")
    df = _clean(df)

    print(f"\n✓ Master DataFrame ready: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df
