import logging
import pandas as pd

def clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the scraped reviews.

    Cleaning means making the data consistent and analysis-ready.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    if df.empty:
        raise ValueError("Input DataFrame is empty. No reviews to clean.")

    required_columns = {"review_id", "review", "rating", "date", "bank", "source"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    original_count = len(df)

    df = df.drop_duplicates(subset=["review_id"])
    after_duplicates = len(df)

    df = df.dropna(subset=["review", "rating"])
    after_missing = len(df)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    df = df[["review", "rating", "date", "bank", "source"]]

    logging.info("Cleaning summary")
    logging.info(f"Original rows: {original_count}")
    logging.info(f"Rows after removing duplicates: {after_duplicates}")
    logging.info(f"Rows after removing missing review/rating: {after_missing}")
    logging.info(f"Final cleaned rows: {len(df)}")

    return df