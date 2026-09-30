import pandas as pd
import os


# Files we want to inspect
files = [
    "data/raw/phonepe_reviews.csv",
    "data/raw/google_pay_reviews.csv",
    "data/raw/paytm_reviews.csv"
]


for file in files:

    print("\n" + "=" * 60)
    print("FILE:", file)
    print("=" * 60)

    # Read CSV
    df = pd.read_csv(file)

    # Number of rows and columns
    print("\nShape:")
    print(df.shape)

    # Column names
    print("\nColumns:")
    print(df.columns.tolist())

    # First 5 rows
    print("\nFirst 5 rows:")
    print(df.head())

    # Missing values
    print("\nMissing values:")
    print(df.isnull().sum())

    # Duplicate rows
    print("\nDuplicate rows:", df.duplicated().sum())

    # Rating distribution
    print("\nRating distribution:")
    print(df["score"].value_counts().sort_index())

    # App versions
    print("\nTop app versions:")
    print(df["appVersion"].value_counts().head(10))