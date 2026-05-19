# Ethiopian Banking App Review Analysis

This project analyzes customer reviews from Ethiopian mobile banking applications available on the Google Play Store. From Commerical Bank of Ethiopia, Dashen Bank and Bank of Abbysiniya.

The project includes:
- Review scraping
- Data cleaning and preprocessing
- Sentiment analysis
- Thematic analysis using TF-IDF and keyword classification

## Objectives

- Collect at least 400 reviews per bank
- Clean and preprocess review data
- Analyze customer sentiment
- Identify recurring customer issues and themes

## Data Source

Reviews were scraped from the Google Play Store using the `google-play-scraper` package.

## project Structure
project/
│
├── data/
│   ├── raw/
│   └── processed/
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
│   │   └── sentiment_analysis.py
│   │
│   └── utils/
│       └── logger.py
│
├── tests/
├── requirements.txt
└── README.md


## Installation 
pip install -r requirements.txt

## How to run
### Task 1
python scripts/scrape_reviews.py

### Task 2
python scripts/run_task2_analysis.py

## Output
## Output Files

- `data/raw/bank_reviews_clean.csv`
- `data/processed/reviews_with_sentiment_themes.csv`
- `reports/sentiment_summary_by_bank.csv`
- `reports/theme_summary_by_bank.csv`
- `reports/task2_insights.md`

## Methodology
scraping
cleaning
VADER sentiment
TF-IDF keywords
rule-based themes

## Limitations

- Google Play reviews may contain spam or duplicated opinions.
- VADER may not fully capture sarcasm or multilingual sentiment.
- Theme assignment is keyword-based and may oversimplify some reviews.