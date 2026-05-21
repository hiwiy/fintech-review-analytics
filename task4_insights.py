import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from sqlalchemy import create_engine
from wordcloud import WordCloud


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

engine = create_engine(DATABASE_URL)

OUTPUT_DIR = Path("outputs/task4")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")


def load_reviews():
    query = """
        SELECT
            r.review_id,
            b.bank_name,
            r.review_text,
            r.rating,
            r.review_date,
            r.sentiment_label,
            r.sentiment_score,
            r.identified_theme,
            r.source
        FROM reviews r
        JOIN banks b
            ON r.bank_id = b.bank_id;
    """

    df = pd.read_sql(query, engine)

    df["review_date"] = pd.to_datetime(df["review_date"])
    df["sentiment_label"] = df["sentiment_label"].fillna("unknown")
    df["identified_theme"] = df["identified_theme"].fillna("unknown")

    return df


def save_summary_tables(df):
    bank_summary = df.groupby("bank_name").agg(
        total_reviews=("review_id", "count"),
        average_rating=("rating", "mean"),
        average_sentiment_score=("sentiment_score", "mean")
    ).reset_index()

    bank_summary["average_rating"] = bank_summary["average_rating"].round(2)
    bank_summary["average_sentiment_score"] = bank_summary["average_sentiment_score"].round(3)

    sentiment_summary = (
        df.groupby(["bank_name", "sentiment_label"])
        .size()
        .reset_index(name="count")
    )

    theme_summary = (
        df.groupby(["bank_name", "identified_theme"])
        .size()
        .reset_index(name="count")
        .sort_values(["bank_name", "count"], ascending=[True, False])
    )

    bank_summary.to_csv(OUTPUT_DIR / "bank_summary.csv", index=False)
    sentiment_summary.to_csv(OUTPUT_DIR / "sentiment_summary.csv", index=False)
    theme_summary.to_csv(OUTPUT_DIR / "theme_summary.csv", index=False)

    print("\nBank Summary")
    print(bank_summary)

    print("\nTop Themes")
    print(theme_summary.groupby("bank_name").head(10))

    return bank_summary, sentiment_summary, theme_summary


def plot_sentiment_distribution(df):
    sentiment_counts = (
        df.groupby(["bank_name", "sentiment_label"])
        .size()
        .reset_index(name="count")
    )

    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=sentiment_counts,
        x="bank_name",
        y="count",
        hue="sentiment_label"
    )

    plt.title("Sentiment Distribution by Bank")
    plt.xlabel("Bank")
    plt.ylabel("Number of Reviews")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "sentiment_distribution_by_bank.png", dpi=300)
    plt.close()


def plot_average_rating(df):
    rating_summary = (
        df.groupby("bank_name")["rating"]
        .mean()
        .reset_index()
        .sort_values("rating", ascending=False)
    )

    plt.figure(figsize=(9, 6))
    sns.barplot(
        data=rating_summary,
        x="bank_name",
        y="rating"
    )

    plt.title("Average Rating by Bank")
    plt.xlabel("Bank")
    plt.ylabel("Average Rating")
    plt.ylim(0, 5)
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "average_rating_by_bank.png", dpi=300)
    plt.close()


def plot_rating_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(
        data=df,
        x="bank_name",
        y="rating"
    )

    plt.title("Rating Distribution by Bank")
    plt.xlabel("Bank")
    plt.ylabel("Rating")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "rating_distribution_by_bank.png", dpi=300)
    plt.close()


def plot_theme_frequency(df):
    theme_counts = (
        df[df["identified_theme"] != "unknown"]
        .groupby(["bank_name", "identified_theme"])
        .size()
        .reset_index(name="count")
    )

    for bank in theme_counts["bank_name"].unique():
        bank_themes = (
            theme_counts[theme_counts["bank_name"] == bank]
            .sort_values("count", ascending=False)
            .head(10)
        )

        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=bank_themes,
            x="count",
            y="identified_theme"
        )

        plt.title(f"Top Themes for {bank}")
        plt.xlabel("Number of Reviews")
        plt.ylabel("Theme")
        plt.tight_layout()

        filename = bank.lower().replace(" ", "_").replace("/", "_")
        plt.savefig(OUTPUT_DIR / f"top_themes_{filename}.png", dpi=300)
        plt.close()


def plot_sentiment_trend(df):
    trend_df = df.copy()
    trend_df["month"] = trend_df["review_date"].dt.to_period("M").dt.to_timestamp()

    monthly_sentiment = (
        trend_df.groupby(["month", "bank_name"])["sentiment_score"]
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(12, 6))
    sns.lineplot(
        data=monthly_sentiment,
        x="month",
        y="sentiment_score",
        hue="bank_name",
        marker="o"
    )

    plt.title("Average Sentiment Trend Over Time")
    plt.xlabel("Month")
    plt.ylabel("Average Sentiment Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "sentiment_trend_over_time.png", dpi=300)
    plt.close()


def generate_wordclouds(df):
    for bank in df["bank_name"].unique():
        text = " ".join(
            df[df["bank_name"] == bank]["review_text"]
            .dropna()
            .astype(str)
            .tolist()
        )

        if not text.strip():
            continue

        wordcloud = WordCloud(
            width=1200,
            height=700,
            background_color="white",
            max_words=100
        ).generate(text)

        plt.figure(figsize=(12, 7))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title(f"Review Word Cloud for {bank}")
        plt.tight_layout()

        filename = bank.lower().replace(" ", "_").replace("/", "_")
        plt.savefig(OUTPUT_DIR / f"wordcloud_{filename}.png", dpi=300)
        plt.close()


def extract_drivers_and_pain_points(df):
    results = []

    for bank in df["bank_name"].unique():
        bank_df = df[df["bank_name"] == bank]

        drivers = (
            bank_df[
                (bank_df["sentiment_label"].str.lower() == "positive") |
                (bank_df["rating"] >= 4)
            ]
            .groupby("identified_theme")
            .size()
            .reset_index(name="count")
            .sort_values("count", ascending=False)
            .head(5)
        )

        pain_points = (
            bank_df[
                (bank_df["sentiment_label"].str.lower() == "negative") |
                (bank_df["rating"] <= 2)
            ]
            .groupby("identified_theme")
            .size()
            .reset_index(name="count")
            .sort_values("count", ascending=False)
            .head(5)
        )

        for _, row in drivers.iterrows():
            if row["identified_theme"] != "unknown":
                results.append({
                    "bank_name": bank,
                    "type": "satisfaction_driver",
                    "theme": row["identified_theme"],
                    "evidence_count": row["count"]
                })

        for _, row in pain_points.iterrows():
            if row["identified_theme"] != "unknown":
                results.append({
                    "bank_name": bank,
                    "type": "pain_point",
                    "theme": row["identified_theme"],
                    "evidence_count": row["count"]
                })

    result_df = pd.DataFrame(results)
    result_df.to_csv(OUTPUT_DIR / "drivers_and_pain_points.csv", index=False)

    print("\nDrivers and Pain Points")
    print(result_df)

    return result_df


def generate_recommendation_template(drivers_pain_points):
    lines = []

    for bank in drivers_pain_points["bank_name"].unique():
        bank_df = drivers_pain_points[drivers_pain_points["bank_name"] == bank]

        pain_points = bank_df[bank_df["type"] == "pain_point"].head(3)
        drivers = bank_df[bank_df["type"] == "satisfaction_driver"].head(3)

        lines.append(f"\n## {bank}")
        lines.append("\n### Satisfaction Drivers")
        for _, row in drivers.iterrows():
            lines.append(f"- {row['theme']} appeared in {row['evidence_count']} positive/high-rating reviews.")

        lines.append("\n### Pain Points")
        for _, row in pain_points.iterrows():
            lines.append(f"- {row['theme']} appeared in {row['evidence_count']} negative/low-rating reviews.")

        lines.append("\n### Recommended Improvements")
        lines.append("- Improve the most frequent pain-point theme through targeted product fixes and QA testing.")
        lines.append("- Strengthen customer support messaging around the most common negative review topics.")
        lines.append("- Preserve and promote the strongest satisfaction driver in future app updates.")

    with open(OUTPUT_DIR / "recommendation_notes.md", "w", encoding="utf-8") as file:
        file.write("\n".join(lines))


def main():
    df = load_reviews()

    print(f"Loaded {len(df)} reviews from Neon PostgreSQL.")

    save_summary_tables(df)

    plot_sentiment_distribution(df)
    plot_average_rating(df)
    plot_rating_distribution(df)
    plot_theme_frequency(df)
    plot_sentiment_trend(df)
    generate_wordclouds(df)

    drivers_pain_points = extract_drivers_and_pain_points(df)
    generate_recommendation_template(drivers_pain_points)

    print(f"\nTask 4 outputs saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()