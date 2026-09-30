import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
file = "data/processed/upi_reviews_cleaned.csv"
df = pd.read_csv(file)

# --------------------------------
# 1. Rating Distribution
# --------------------------------

rating_counts = df["rating"].value_counts().sort_index()

plt.figure(figsize=(8, 5))
rating_counts.plot(kind="bar")

plt.title("UPI App Review Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig("data/processed/rating_distribution.png")
plt.show()


# --------------------------------
# 2. Average Rating by App
# --------------------------------

avg_rating = df.groupby("app")["rating"].mean().sort_values()

plt.figure(figsize=(8, 5))
avg_rating.plot(kind="bar")

plt.title("Average Rating by UPI App")
plt.xlabel("App")
plt.ylabel("Average Rating")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig("data/processed/average_rating_by_app.png")
plt.show()


# --------------------------------
# 3. Reviews by App
# --------------------------------

review_counts = df["app"].value_counts()

plt.figure(figsize=(8, 5))
review_counts.plot(kind="bar")

plt.title("Number of Reviews by App")
plt.xlabel("App")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig("data/processed/reviews_by_app.png")
plt.show()