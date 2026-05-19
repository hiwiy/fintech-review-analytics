# Task 2: Sentiment and Thematic Analysis Summary

## Overview

This analysis was conducted on cleaned Google Play Store reviews for the selected Ethiopian banking applications.

Total reviews analyzed: 1200

## Sentiment Analysis

The most common sentiment category is **positive**.

Sentiment was calculated using VADER sentiment analysis. Each review was assigned:

- `sentiment_score`
- `sentiment_label`

The sentiment labels are:

- positive
- neutral
- negative

## Thematic Analysis

The most common theme is **General Feedback**.

Themes were assigned using keyword-based rules informed by common mobile banking issues, such as login problems, transaction issues, app performance, customer support, and user interface feedback.

## Top TF-IDF Keywords

The top extracted keywords are:

app, bank, banking, best, dashen, easy, fast, fix, good, like, mobile, nice, service, super, time, update, use, work, working, worst

## Output Files

The analysis generated the following files:

- `data/processed/reviews_with_sentiment_themes.csv`
- `reports/sentiment_summary_by_bank.csv`
- `reports/theme_summary_by_bank.csv`

## Limitations

VADER is a lightweight sentiment model and may not fully understand sarcasm, mixed-language reviews, or banking-specific context.  
The theme classification is rule-based, so some reviews may be assigned broad themes rather than highly specific issue categories.