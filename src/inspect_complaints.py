import pandas as pd

# Load cleaned data
file = "data/processed/upi_reviews_cleaned.csv"
df = pd.read_csv(file)

# Show 1-star and 2-star reviews
complaints = df[df["rating"] <= 2].copy()

print("=" * 70)
print("LOW-RATED REVIEWS / POTENTIAL COMPLAINTS")
print("=" * 70)

print("\nTotal low-rated reviews:", len(complaints))

# Show app and review text
for _, row in complaints.iterrows():
    print("\n" + "-" * 70)
    print("APP:", row["app"])
    print("RATING:", row["rating"])
    print("VERSION:", row["app_version"])
    print("REVIEW:", row["review_text"])

print("\n" + "=" * 70)
print("INSPECTION COMPLETED")
print("=" * 70)