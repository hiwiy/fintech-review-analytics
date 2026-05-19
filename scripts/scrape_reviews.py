import logging
import pandas as pd

from src.scraping.scraper import scrape_bank_reviews
from src.preprocessing.clean_reviews import clean_reviews


BANK_APPS = {
    "Commercial Bank of Ethiopia": "com.combanketh.mobilebanking",
    "Bank of Abyssinia": "com.boa.boaMobileBanking",
    "Dashen Bank": "com.dashen.dashensuperapp",
}


def main():

    all_reviews = []

    for bank_name, app_id in BANK_APPS.items():

        bank_df = scrape_bank_reviews(
            bank_name,
            app_id,
            count=400,
        )

        if not bank_df.empty:
            all_reviews.append(bank_df)

    combined_df = pd.concat(all_reviews, ignore_index=True)

    clean_df = clean_reviews(combined_df)

    clean_df.to_csv(
        "data/raw/bank_reviews_clean.csv",
        index=False
    )

    logging.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()