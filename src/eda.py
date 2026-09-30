import pandas as pd

# Load cleaned data
file = "data/processed/upi_reviews_cleaned.csv"

df = pd.read_csv(file)

print("=" * 60)
print("UPI COMPLAINT INTELLIGENCE - EDA")
print("=" * 60)

# 1. Dataset shape
print("\nDataset Shape:")
print(df.shape)

# 2. Apps
print("\nReviews by App:")
print(df["app"].value_counts())

# 3. Ratings
print("\nRating Distribution:")
print(df["rating"].value_counts().sort_index())

# 4. Average rating by app
print("\nAverage Rating by App:")
print(df.groupby("app")["rating"].mean().round(2))

# 5. Review date range
print("\nReview Date Range:")
print("Start:", df["review_date"].min())
print("End:", df["review_date"].max())

# 6. Reviews by app version
print("\nTop App Versions:")
print(df["app_version"].value_counts().head(10))

print("\nEDA completed!")