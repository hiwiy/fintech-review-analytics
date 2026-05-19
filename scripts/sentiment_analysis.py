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
REPORTS_DIR = Path("reports")


def classify_sentiment(score: float) -> str:
    if score >= 0.05:
        return "positive"
    if score <= -0.05:
        return "negative"
    return "neutral"


def assign_theme(review: str) -> str:
    text = str(review).lower()

    if any(word in text for word in ["login", "password", "otp", "pin", "account"]):
        return "Account Access"

    if any(word in text for word in ["transfer", "transaction", "payment", "send", "receive"]):
        return "Transactions"

    if any(word in text for word in ["slow", "loading", "crash", "bug", "error", "fail"]):
        return "App Performance"

    if any(word in text for word in ["support", "service", "help", "customer"]):
        return "Customer Support"

    if any(word in text for word in ["update", "feature", "ui", "interface", "design"]):
        return "Features and UI"

    return "General Feedback"


def extract_top_keywords(df: pd.DataFrame, text_column: str = "review", max_features: int = 20) -> list[str]:
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=max_features
    )

    vectorizer.fit_transform(df[text_column].astype(str))
    return list(vectorizer.get_feature_names_out())


def create_summary_reports(df: pd.DataFrame) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    sentiment_summary = (
        df.groupby(["bank", "sentiment_label"])
        .size()
        .reset_index(name="review_count")
    )

    theme_summary = (
        df.groupby(["bank", "identified_theme"])
        .size()
        .reset_index(name="review_count")
        .sort_values(["bank", "review_count"], ascending=[True, False])
    )

    sentiment_summary.to_csv(REPORTS_DIR / "sentiment_summary_by_bank.csv", index=False)
    theme_summary.to_csv(REPORTS_DIR / "theme_summary_by_bank.csv", index=False)

    top_keywords = extract_top_keywords(df)

    most_common_sentiment = df["sentiment_label"].value_counts().idxmax()
    most_common_theme = df["identified_theme"].value_counts().idxmax()

    insight_text = f"""
# Task 2: Sentiment and Thematic Analysis Summary

## Overview

This analysis was conducted on cleaned Google Play Store reviews for the selected Ethiopian banking applications.

Total reviews analyzed: {len(df)}

## Sentiment Analysis

The most common sentiment category is **{most_common_sentiment}**.

Sentiment was calculated using VADER sentiment analysis. Each review was assigned:

- `sentiment_score`
- `sentiment_label`

The sentiment labels are:

- positive
- neutral
- negative

## Thematic Analysis

The most common theme is **{most_common_theme}**.

Themes were assigned using keyword-based rules informed by common mobile banking issues, such as login problems, transaction issues, app performance, customer support, and user interface feedback.

## Top TF-IDF Keywords

The top extracted keywords are:

{", ".join(top_keywords)}

## Output Files

The analysis generated the following files:

- `data/processed/reviews_with_sentiment_themes.csv`
- `reports/sentiment_summary_by_bank.csv`
- `reports/theme_summary_by_bank.csv`

## Limitations

VADER is a lightweight sentiment model and may not fully understand sarcasm, mixed-language reviews, or banking-specific context.  
The theme classification is rule-based, so some reviews may be assigned broad themes rather than highly specific issue categories.
"""

    with open(REPORTS_DIR / "task2_insights.md", "w", encoding="utf-8") as file:
        file.write(insight_text.strip())


def main() -> None:
    try:
        logging.info("Loading cleaned review data...")
        df = pd.read_csv(INPUT_PATH)

        if df.empty:
            raise ValueError("The input dataset is empty.")

        required_columns = {"review", "rating", "date", "bank", "source"}
        missing_columns = required_columns - set(df.columns)

        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        logging.info("Running sentiment analysis...")
        analyzer = SentimentIntensityAnalyzer()

        df["sentiment_score"] = df["review"].astype(str).apply(
            lambda text: analyzer.polarity_scores(text)["compound"]
        )

        df["sentiment_label"] = df["sentiment_score"].apply(classify_sentiment)

        logging.info("Assigning themes...")
        df["identified_theme"] = df["review"].apply(assign_theme)

        logging.info("Saving enriched Task 2 dataset...")
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

        logging.info("Creating summary reports...")
        report_df = df.rename(columns={"review_text": "review"})
        create_summary_reports(report_df)

        logging.info("Task 2 analysis completed successfully.")

    except FileNotFoundError:
        logging.error(f"Input file not found: {INPUT_PATH}")

    except ValueError as error:
        logging.error(f"Validation error: {error}")

    except Exception as error:
        logging.error(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()