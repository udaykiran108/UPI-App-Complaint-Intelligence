import pandas as pd

file = "data/processed/upi_reviews_classified.csv"

df = pd.read_csv(file)

print("=" * 70)
print("UPI COMPLAINT INTELLIGENCE - CLASSIFICATION VALIDATION")
print("=" * 70)

print("\nDataset Shape:")
print(df.shape)

print("\nMissing Values:")
print(df[["topic", "sentiment"]].isnull().sum())

print("\nTopic Distribution:")
print(df["topic"].value_counts())

print("\nSentiment Distribution:")
print(df["sentiment"].value_counts())

print("\nTopic by App:")
print(
    pd.crosstab(
        df["app"],
        df["topic"]
    )
)

print("\nSentiment by App:")
print(
    pd.crosstab(
        df["app"],
        df["sentiment"]
    )
)

print("\nUnique Topics:")
print(df["topic"].unique())

print("\nUnique Sentiments:")
print(df["sentiment"].unique())

print("\nValidation completed!")