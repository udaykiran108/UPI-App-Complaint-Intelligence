import pandas as pd

file = "data/processed/upi_reviews_classified.csv"

df = pd.read_csv(file)

other = df[df["topic"] == "Other"]

print("=" * 70)
print("REVIEWS CLASSIFIED AS OTHER")
print("=" * 70)

print(f"\nTotal Other reviews: {len(other)}")

print("\nReviews by App:")
print(other["app"].value_counts())

print("\nSample of Other reviews:")

for _, row in other.head(30).iterrows():

    print("\n" + "-" * 70)
    print("APP:", row["app"])
    print("RATING:", row["rating"])
    print("SENTIMENT:", row["sentiment"])
    print("REVIEW:", row["review_text"])

print("\n" + "=" * 70)
print("INSPECTION COMPLETED")
print("=" * 70)