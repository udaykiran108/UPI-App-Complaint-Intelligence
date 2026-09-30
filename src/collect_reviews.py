from google_play_scraper import reviews, Sort
import pandas as pd
import os


# Create raw data folder if it doesn't exist
os.makedirs("data/raw", exist_ok=True)


# Apps we want to analyze
apps = {
    "PhonePe": "com.phonepe.app",
    "Google Pay": "com.google.android.apps.walletnfcrel",
    "Paytm": "net.one97.paytm"
}


# Collect reviews
for app_name, app_id in apps.items():

    print(f"\nCollecting reviews for {app_name}...")

    result, continuation_token = reviews(
        app_id,
        lang="en",
        country="in",
        sort=Sort.NEWEST,
        count=100
    )

    # Convert to DataFrame
    df = pd.DataFrame(result)

    # Keep the important columns
    columns = [
        "reviewId",
        "userName",
        "content",
        "score",
        "at",
        "appVersion"
    ]

    df = df[columns]

    # Add app name
    df["app"] = app_name

    # Save CSV
    filename = f"data/raw/{app_name.lower().replace(' ', '_')}_reviews.csv"

    df.to_csv(filename, index=False)

    print(f"Saved {len(df)} reviews to {filename}")


print("\nAll apps completed!")