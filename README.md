# Ethiopian Banking App Review Analysis

This project analyzes customer reviews from major Ethiopian mobile banking applications available on the Google Play Store, including:

- Commercial Bank of Ethiopia (CBE)
- Dashen Bank
- Bank of Abyssinia (BOA)

The project covers the complete analytics pipeline from review collection to sentiment analysis, thematic extraction, PostgreSQL storage, and customer insight visualization.

---

# Project Objectives

The main objectives of this project are to:

- Collect and analyze customer reviews from banking mobile applications
- Clean and preprocess raw review data
- Perform sentiment analysis on customer feedback
- Identify recurring customer experience themes
- Store processed data in PostgreSQL (Neon.tech)
- Generate business insights and visual analytics
- Recommend improvement opportunities for banking apps

---

# Features

## Task 1 — Review Scraping

- Scraped Google Play Store reviews using `google-play-scraper`
- Collected 400+ reviews per bank
- Stored raw review data in CSV format

## Task 2 — Data Cleaning & NLP Analysis

- Removed duplicates and missing values
- Standardized review text
- Performed sentiment analysis using VADER
- Extracted themes using TF-IDF and keyword classification

## Task 3 — PostgreSQL Database Integration

- Designed relational database schema
- Integrated Neon PostgreSQL cloud database
- Loaded processed review data into PostgreSQL
- Performed SQL-based validation and integrity checks

## Task 4 — Customer Insight Analysis & Visualization

- Generated sentiment distribution analysis
- Created rating comparison visualizations
- Analyzed customer pain points and satisfaction drivers
- Generated trend analysis and word clouds
- Produced actionable recommendation summaries

---

# Technologies Used

- Python
- Pandas
- NumPy
- SQLAlchemy
- PostgreSQL (Neon.tech)
- Matplotlib
- Seaborn
- Scikit-learn
- NLTK
- WordCloud

---

# Data Source

Customer reviews were collected from the Google Play Store using the `google-play-scraper` package.

---

# Project Structure

```text
project/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── outputs/
│   └── task4/
│
├── reports/
│
├── scripts/
│   ├── scrape_reviews.py
│   └── run_task2_analysis.py
│
├── src/
│   ├── scraping/
│   │   └── scraper.py
│   │
│   ├── preprocessing/
│   │   └── clean_reviews.py
│   │
│   ├── analysis/
│   │   ├── sentiment_analysis.py
│   │   └── theme_analysis.py
│   │
│   └── utils/
│       └── logger.py
│
├── create_tables.py
├── load_to_neon.py
├── verify_neon.py
├── task4_insights.py
├── schema.sql
├── requirements.txt
├── .env.example
└── README.md
```

---

# Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd <repository-name>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=your_neon_postgresql_connection_string
```

Example:

```env
DATABASE_URL=postgresql+psycopg2://username:password@host.neon.tech/dbname?sslmode=require
```

---

# How to Run

## Task 1 — Scrape Reviews

```bash
python scripts/scrape_reviews.py
```

## Task 2 — Sentiment & Theme Analysis

```bash
python scripts/run_task2_analysis.py
```

## Task 3 — PostgreSQL Integration

### Create Tables

```bash
python create_tables.py
```

### Load Data into Neon PostgreSQL

```bash
python load_to_neon.py
```

### Verify Database Records

```bash
python verify_neon.py
```

## Task 4 — Insights & Visualization

```bash
python task4_insights.py
```

---

# Output Files

## Processed Data

- `data/raw/bank_reviews_clean.csv`
- `data/processed/reviews_with_sentiment_themes.csv`

## Database

PostgreSQL tables:

- `banks`
- `reviews`

## Reports & Insights

- `reports/sentiment_summary_by_bank.csv`
- `reports/theme_summary_by_bank.csv`
- `reports/task2_insights.md`

## Task 4 Visualizations

- `outputs/task4/average_rating_by_bank.png`
- `outputs/task4/rating_distribution_by_bank.png`
- `outputs/task4/sentiment_distribution_by_bank.png`
- `outputs/task4/sentiment_trend_over_time.png`
- `outputs/task4/wordcloud_<bank>.png`
- `outputs/task4/top_themes_<bank>.png`

## Analytical Summaries

- `outputs/task4/bank_summary.csv`
- `outputs/task4/sentiment_summary.csv`
- `outputs/task4/theme_summary.csv`
- `outputs/task4/drivers_and_pain_points.csv`
- `outputs/task4/recommendation_notes.md`

---

# Methodology

## Review Collection

- Google Play review scraping
- Multi-bank review aggregation

## Data Preprocessing

- Duplicate removal
- Missing value handling
- Text normalization
- Date formatting

## Sentiment Analysis

- VADER sentiment scoring
- Sentiment classification:
  - Positive
  - Neutral
  - Negative

## Theme Analysis

- TF-IDF keyword extraction
- Rule-based thematic categorization

## Database Engineering

- Relational schema design
- PostgreSQL normalization
- Data integrity validation

## Insight Generation

- Customer pain-point analysis
- Satisfaction-driver extraction
- Trend visualization
- Comparative bank analysis

---

# Key Insights

The analysis revealed several recurring themes across Ethiopian banking applications.

## Common Customer Pain Points

- App crashes and instability
- Login/authentication issues
- Slow transaction processing
- Poor customer support responsiveness

## Common Satisfaction Drivers

- Easy fund transfers
- User-friendly interfaces
- Fast transaction notifications
- Improved app performance updates

---

# Limitations

- Google Play reviews may contain spam or duplicate opinions
- VADER may not fully capture sarcasm or multilingual sentiment
- Theme classification is keyword-based and may oversimplify context
- Review distribution across banks may not be perfectly balanced

---

# Future Improvements

- Deploy interactive dashboards using Streamlit or Power BI
- Use transformer-based NLP models (BERT)
- Add multilingual sentiment analysis
- Implement automated ETL pipelines
- Introduce real-time review monitoring

---

# Author

hiwiy.