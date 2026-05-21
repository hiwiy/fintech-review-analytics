import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

engine = create_engine(DATABASE_URL)

queries = {
    "Total banks": """
        SELECT COUNT(*) AS total_banks
        FROM banks;
    """,

    "Total reviews": """
        SELECT COUNT(*) AS total_reviews
        FROM reviews;
    """,

    "Reviews per bank": """
        SELECT 
            b.bank_name,
            COUNT(r.review_id) AS total_reviews
        FROM banks b
        LEFT JOIN reviews r
            ON b.bank_id = r.bank_id
        GROUP BY b.bank_name
        ORDER BY total_reviews DESC;
    """,

    "Average rating per bank": """
        SELECT 
            b.bank_name,
            ROUND(AVG(r.rating)::numeric, 2) AS average_rating
        FROM banks b
        JOIN reviews r
            ON b.bank_id = r.bank_id
        GROUP BY b.bank_name
        ORDER BY average_rating DESC;
    """,

    "Sentiment distribution": """
        SELECT 
            b.bank_name,
            r.sentiment_label,
            COUNT(*) AS total_reviews
        FROM reviews r
        JOIN banks b
            ON r.bank_id = b.bank_id
        GROUP BY b.bank_name, r.sentiment_label
        ORDER BY b.bank_name, total_reviews DESC;
    """,

    "Theme distribution": """
        SELECT 
            b.bank_name,
            r.identified_theme,
            COUNT(*) AS total_reviews
        FROM reviews r
        JOIN banks b
            ON r.bank_id = b.bank_id
        GROUP BY b.bank_name, r.identified_theme
        ORDER BY b.bank_name, total_reviews DESC;
    """,

    "Data quality check": """
        SELECT
            COUNT(*) FILTER (WHERE review_id IS NULL) AS missing_review_id,
            COUNT(*) FILTER (WHERE bank_id IS NULL) AS missing_bank_id,
            COUNT(*) FILTER (WHERE review_text IS NULL OR TRIM(review_text) = '') AS missing_review_text,
            COUNT(*) FILTER (WHERE rating IS NULL) AS missing_rating,
            COUNT(*) FILTER (WHERE review_date IS NULL) AS missing_review_date,
            COUNT(*) FILTER (WHERE source IS NULL OR TRIM(source) = '') AS missing_source
        FROM reviews;
    """
}

with engine.connect() as conn:
    for title, query in queries.items():
        print("\n" + "=" * 60)
        print(title)
        print("=" * 60)

        result = conn.execute(text(query)).mappings().all()

        for row in result:
            print(dict(row))