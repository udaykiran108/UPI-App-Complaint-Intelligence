# UPI App Complaint Intelligence: What’s Breaking for Users?

## 📌 Project Overview

This project analyzes user reviews of three popular UPI payment applications — **PhonePe, Google Pay, and Paytm** — to understand what users are complaining about, how sentiment differs across apps, and which complaint topics appear most frequently.

The project combines **Python, LLM-based text classification, BigQuery SQL, and Looker Studio** to transform raw Google Play reviews into actionable customer insights.

---

## 🎯 Business Problem

UPI applications receive a large volume of user feedback through app-store reviews. Manually analyzing these reviews makes it difficult to quickly identify recurring problems.

This project aims to answer:

- What are users complaining about most?
- How does complaint sentiment differ across UPI apps?
- Which complaint topics are most common for each app?
- Are there differences in complaint patterns between app versions?
- Can SQL and dashboards be used to turn unstructured reviews into useful business insights?

---

## 📱 Apps Analyzed

The analysis covers:

- **PhonePe**
- **Google Pay**
- **Paytm**

A total of **300 Google Play reviews** were collected:

| App | Reviews |
|---|---:|
| PhonePe | 100 |
| Google Pay | 100 |
| Paytm | 100 |
| **Total** | **300** |

---

## 🛠️ Technologies Used

### Data Collection
- Python
- `google-play-scraper`

### Data Processing & Analysis
- Pandas
- NumPy
- Matplotlib
- Python

### Text Classification
- LLM-based classification
- Groq API
- `openai/gpt-oss-120b`

### Data Warehouse & SQL
- Google BigQuery
- Standard SQL
- JOINs
- CTEs
- GROUP BY
- COUNT
- CASE WHEN
- Window functions
- RANK / ROW_NUMBER
- PARTITION BY
- ORDER BY

### Visualization
- Looker Studio

---

## 📂 Project Structure

```text
UPI Complaint Intelligence/
│
├── data/
│   ├── raw/
│   │   ├── phonepe_reviews.csv
│   │   ├── google_pay_reviews.csv
│   │   └── paytm_reviews.csv
│   │
│   └── processed/
│       ├── upi_reviews_cleaned.csv
│       ├── upi_reviews_classified.csv
│       ├── rating_distribution.png
│       ├── average_rating_by_app.png
│       └── reviews_by_app.png
│
├── notebooks/
│
├── src/
│   ├── test_scraper.py
│   ├── collect_reviews.py
│   ├── clean_reviews.py
│   ├── eda.py
│   ├── eda_visuals.py
│   ├── inspect_complaints.py
│   ├── inspect_other.py
│   ├── test_groq.py
│   ├── test_groq_classification.py
│   ├── classify_all_reviews_groq.py
│   └── validate_classification.py
│
├── dashboard/
│
├── README.md
└── requirements.txt