import logging
import pandas as pd
from google_play_scraper import reviews, Sort


def scrape_bank_reviews(bank_name: str, app_id: str, count: int = 400) -> pd.DataFrame:

    try:
        logging.info(f"Scraping reviews for {bank_name}")

        result, _ = reviews(
            app_id,
            lang="en",
            country="et",
            sort=Sort.NEWEST,
            count=count,
        )

        if not result:
            logging.warning(f"No reviews found for {bank_name}")
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

        return pd.DataFrame(rows)

    except Exception as error:
        logging.error(f"Scraping failed for {bank_name}: {error}")
        return pd.DataFrame()