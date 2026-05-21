import hashlib
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

engine = create_engine(DATABASE_URL)


CSV_PATH = "data/processed/reviews_with_sentiment_themes.csv"


def generate_review_id(row):
    raw = f"{row['bank']}|{row['review_date']}|{row['rating']}|{row['review_text']}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def clean_dataframe(csv_path):
    df = pd.read_csv(csv_path)

    df.columns = [col.strip().lower() for col in df.columns]

    df = df.rename(columns={
        "review": "review_text",
        "date": "review_date",
        "bank_name": "bank",
        "theme": "identified_theme"
    })

    required_columns = ["review_text", "rating", "review_date", "bank"]
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if "source" not in df.columns:
        df["source"] = "Google Play"

    if "sentiment_label" not in df.columns:
        df["sentiment_label"] = None

    if "sentiment_score" not in df.columns:
        df["sentiment_score"] = None

    if "identified_theme" not in df.columns:
        df["identified_theme"] = None

    df = df.dropna(subset=["review_text", "rating", "review_date", "bank"])

    df["review_text"] = df["review_text"].astype(str).str.strip()
    df = df[df["review_text"] != ""]

    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df[df["rating"].between(1, 5)]
    df["rating"] = df["rating"].astype(int)

    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce").dt.date

    df["bank"] = df["bank"].astype(str).str.strip()
    df["source"] = df["source"].fillna("Google Play").astype(str).str.strip()

    df["review_id"] = df.apply(generate_review_id, axis=1)

    df = df.drop_duplicates(subset=["review_id"])

    return df


def insert_banks(df):
    banks = sorted(df["bank"].dropna().unique())

    with engine.begin() as conn:
        for bank in banks:
            conn.execute(
                text("""
                    INSERT INTO banks (bank_name, app_name)
                    VALUES (:bank_name, :app_name)
                    ON CONFLICT (bank_name) DO NOTHING;
                """),
                {
                    "bank_name": bank,
                    "app_name": bank
                }
            )


def insert_reviews(df):
    with engine.begin() as conn:
        bank_rows = conn.execute(
            text("SELECT bank_id, bank_name FROM banks;")
        ).fetchall()

        bank_map = {row.bank_name: row.bank_id for row in bank_rows}

        records = []

        for _, row in df.iterrows():
            sentiment_score = row["sentiment_score"]

            if pd.isna(sentiment_score):
                sentiment_score = None

            records.append({
                "review_id": row["review_id"],
                "bank_id": bank_map[row["bank"]],
                "review_text": row["review_text"],
                "rating": int(row["rating"]),
                "review_date": row["review_date"],
                "sentiment_label": row["sentiment_label"],
                "sentiment_score": sentiment_score,
                "identified_theme": row["identified_theme"],
                "source": row["source"]
            })

        conn.execute(
            text("""
                INSERT INTO reviews (
                    review_id,
                    bank_id,
                    review_text,
                    rating,
                    review_date,
                    sentiment_label,
                    sentiment_score,
                    identified_theme,
                    source
                )
                VALUES (
                    :review_id,
                    :bank_id,
                    :review_text,
                    :rating,
                    :review_date,
                    :sentiment_label,
                    :sentiment_score,
                    :identified_theme,
                    :source
                )
                ON CONFLICT (review_id) DO UPDATE SET
                    bank_id = EXCLUDED.bank_id,
                    review_text = EXCLUDED.review_text,
                    rating = EXCLUDED.rating,
                    review_date = EXCLUDED.review_date,
                    sentiment_label = EXCLUDED.sentiment_label,
                    sentiment_score = EXCLUDED.sentiment_score,
                    identified_theme = EXCLUDED.identified_theme,
                    source = EXCLUDED.source;
            """),
            records
        )


def main():
    csv_file = Path(CSV_PATH)

    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")

    df = clean_dataframe(csv_file)

    insert_banks(df)
    insert_reviews(df)

    print(f"Successfully loaded {len(df)} reviews into Neon PostgreSQL.")


if __name__ == "__main__":
    main()