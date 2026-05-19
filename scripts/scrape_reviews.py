import logging
from pathlib import Path

import pandas as pd
from google_play_scraper import reviews, Sort


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


BANK_APPS = {
    "Commercial Bank of Ethiopia": "com.combanketh.mobilebanking",
    "Bank of Abyssinia": "com.boa.boaMobileBanking",
    "Dashen Bank": "com.dashen.dashensuperapp",
}


def scrape_bank_reviews(bank_name: str, app_id: str, count: int = 400) -> pd.DataFrame:
    """
    Scrape reviews for one bank app from Google Play.
    """

    if not bank_name:
        raise ValueError("bank_name cannot be empty")

    if not app_id:
        raise ValueError("app_id cannot be empty")

    if count <= 0:
        raise ValueError("count must be greater than zero")

    try:
        logging.info(f"Scraping reviews for {bank_name}...")

        result, continuation_token = reviews(
            app_id,
            lang="en",
            country="et",
            sort=Sort.NEWEST,
            count=count,
        )

        if not result:
            logging.warning(f"No reviews returned for {bank_name}")
            return pd.DataFrame()

        rows = []

        for item in result:
            rows.append(
                {
                    "review_id": item.get("reviewId"),
                    "review": item.get("content"),
                    "rating": item.get("score"),
                    "date": item.get("at"),
                    "bank": bank_name,
                    "source": "Google Play",
                }
            )

        bank_df = pd.DataFrame(rows)

        logging.info(f"Collected {len(bank_df)} reviews for {bank_name}")

        return bank_df

    except Exception as error:
        logging.error(f"Failed to scrape reviews for {bank_name}: {error}")
        return pd.DataFrame()


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


def save_reviews(df: pd.DataFrame, output_path: str) -> None:
    """
    Save cleaned reviews to CSV.
    """

    try:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(path, index=False)

        logging.info(f"Saved cleaned reviews to {path}")

    except Exception as error:
        logging.error(f"Failed to save reviews to {output_path}: {error}")


def main() -> None:
    all_reviews = []

    for bank_name, app_id in BANK_APPS.items():
        bank_df = scrape_bank_reviews(
            bank_name=bank_name,
            app_id=app_id,
            count=400,
        )

        if bank_df.empty:
            logging.warning(f"Skipping {bank_name} because no reviews were collected.")
            continue

        all_reviews.append(bank_df)

    if not all_reviews:
        logging.error("No reviews collected for any bank. Exiting pipeline.")
        return

    combined_df = pd.concat(all_reviews, ignore_index=True)

    try:
        clean_df = clean_reviews(combined_df)

        output_path = "data/raw/bank_reviews_clean.csv"
        save_reviews(clean_df, output_path)

        logging.info("Preview of cleaned data:")
        logging.info(clean_df.head())

    except Exception as error:
        logging.error(f"Pipeline failed during cleaning or saving: {error}")


if __name__ == "__main__":
    main()