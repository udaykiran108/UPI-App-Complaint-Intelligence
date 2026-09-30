import pandas as pd
import os


# Create processed folder if it doesn't exist
os.makedirs("data/processed", exist_ok=True)


# Raw files
files = [
    "data/raw/phonepe_reviews.csv",
    "data/raw/google_pay_reviews.csv",
    "data/raw/paytm_reviews.csv"
]


# Store cleaned DataFrames
cleaned_data = []


for file in files:

    print(f"\nCleaning: {file}")

    # Read CSV
    df = pd.read_csv(file)

    # Rename columns
    df = df.rename(columns={
        "content": "review_text",
        "score": "rating",
        "at": "review_date",
        "appVersion": "app_version"
    })

    # Convert review date
    df["review_date"] = pd.to_datetime(
        df["review_date"],
        errors="coerce"
    )

    # Remove duplicate review IDs
    df = df.drop_duplicates(subset="reviewId")

    # Remove rows where review text is missing
    df = df.dropna(subset=["review_text"])

    # Clean review text
    df["review_text"] = (
        df["review_text"]
        .astype(str)
        .str.strip()
    )

    # Keep only useful columns
    df = df[
        [
            "reviewId",
            "app",
            "review_text",
            "rating",
            "review_date",
            "app_version"
        ]
    ]

    cleaned_data.append(df)

    print(f"Rows after cleaning: {len(df)}")


# Combine all apps
final_df = pd.concat(
    cleaned_data,
    ignore_index=True
)


# Sort by date
final_df = final_df.sort_values(
    "review_date"
)


# Save processed dataset
output_file = "data/processed/upi_reviews_cleaned.csv"

final_df.to_csv(
    output_file,
    index=False
)


print("\n" + "=" * 60)
print("CLEANING COMPLETED")
print("=" * 60)

print(f"Total rows: {len(final_df)}")

print("\nColumns:")
print(final_df.columns.tolist())

print("\nMissing values:")
print(final_df.isnull().sum())

print(f"\nSaved to: {output_file}")