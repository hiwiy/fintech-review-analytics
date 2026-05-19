import logging
from pathlib import Path

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)


INPUT_PATH = Path("data/raw/bank_reviews_clean.csv")
OUTPUT_PATH = Path("data/processed/reviews_with_sentiment_themes.csv")


def get_sentiment(score: float) -> str:
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    return "neutral"


def assign_theme(review: str) -> str:
    review = str(review).lower()

    if any(word in review for word in ["login", "password", "otp", "pin", "account"]):
        return "Account Access Issues"

    if any(word in review for word in ["transfer", "transaction", "payment", "send money"]):
        return "Transaction Performance"

    if any(word in review for word in ["crash", "slow", "loading", "error", "bug"]):
        return "App Reliability"

    if any(word in review for word in ["support", "service", "help", "customer"]):
        return "Customer Support"

    if any(word in review for word in ["feature", "fingerprint", "update", "interface", "ui"]):
        return "Feature Requests and UI"

    return "General Feedback"


def run_sentiment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    analyzer = SentimentIntensityAnalyzer()

    df["sentiment_score"] = df["review"].apply(
        lambda text: analyzer.polarity_scores(str(text))["compound"]
    )

    df["sentiment_label"] = df["sentiment_score"].apply(get_sentiment)

    return df


def extract_keywords(df: pd.DataFrame, max_features: int = 30) -> list[str]:
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=max_features
    )

    tfidf_matrix = vectorizer.fit_transform(df["review"].astype(str))
    keywords = vectorizer.get_feature_names_out()

    return list(keywords)


def main() -> None:
    try:
        logging.info("Loading cleaned review data...")
        df = pd.read_csv(INPUT_PATH)

        if df.empty:
            raise ValueError("Input dataset is empty.")

        required_columns = {"review", "rating", "date", "bank", "source"}
        missing_columns = required_columns - set(df.columns)

        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        logging.info("Running sentiment analysis...")
        df = run_sentiment_analysis(df)

        logging.info("Assigning themes...")
        df["identified_theme"] = df["review"].apply(assign_theme)

        logging.info("Extracting TF-IDF keywords...")
        keywords = extract_keywords(df)
        logging.info(f"Top keywords: {keywords}")

        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

        df = df.reset_index().rename(columns={"index": "review_id"})
        df = df.rename(columns={"review": "review_text"})

        output_columns = [
            "review_id",
            "review_text",
            "rating",
            "date",
            "bank",
            "source",
            "sentiment_label",
            "sentiment_score",
            "identified_theme"
        ]

        df[output_columns].to_csv(OUTPUT_PATH, index=False)

        logging.info(f"Task 2 output saved to {OUTPUT_PATH}")

    except FileNotFoundError:
        logging.error(f"Input file not found: {INPUT_PATH}")

    except ValueError as error:
        logging.error(f"Data validation error: {error}")

    except Exception as error:
        logging.error(f"Unexpected error while running Task 2: {error}")


if __name__ == "__main__":
    main()