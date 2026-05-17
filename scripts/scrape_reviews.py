import pandas as pd
from google_play_scraper import reviews, Sort


BANK_APPS = {
    "Commercial Bank of Ethiopia": "com.combanketh.mobilebanking",
    "Bank of Abyssinia": "com.boa.boaMobileBanking",
    "Dashen Bank": "com.dashen.dashensuperapp",
}


def scrape_bank_reviews(bank_name, app_id, count=400):
    """
    Scrape reviews for one bank app from Google Play.

    Concept:
    - bank_name is our human-readable bank name.
    - app_id is the unique Google Play package name.
    - count is how many reviews we want.
    """

    result, continuation_token = reviews(
        app_id,
        lang="en",
        country="et",
        sort=Sort.NEWEST,
        count=count,
    )

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


def clean_reviews(df):
    """
    Clean the scraped reviews.

    Concept:
    Cleaning means making the data consistent and analysis-ready.
    """

    original_count = len(df)

    df = df.drop_duplicates(subset=["review_id"])
    after_duplicates = len(df)

    df = df.dropna(subset=["review", "rating"])
    after_missing = len(df)

    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    df = df[["review", "rating", "date", "bank", "source"]]

    print("Cleaning summary")
    print("----------------")
    print(f"Original rows: {original_count}")
    print(f"Rows after removing duplicates: {after_duplicates}")
    print(f"Rows after removing missing review/rating: {after_missing}")

    return df


def main():
    all_reviews = []

    for bank_name, app_id in BANK_APPS.items():
        print(f"Scraping reviews for {bank_name}...")

        bank_df = scrape_bank_reviews(
            bank_name=bank_name,
            app_id=app_id,
            count=400,
        )

        print(f"Collected {len(bank_df)} reviews for {bank_name}")
        all_reviews.append(bank_df)

    combined_df = pd.concat(all_reviews, ignore_index=True)

    clean_df = clean_reviews(combined_df)

    output_path = "data/raw/bank_reviews_clean.csv"
    clean_df.to_csv(output_path, index=False)

    print(f"Saved cleaned reviews to {output_path}")
    print(clean_df.head())


if __name__ == "__main__":
    main()