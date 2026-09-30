import pandas as pd
from groq import Groq

# Load cleaned reviews
file = "data/processed/upi_reviews_cleaned.csv"
df = pd.read_csv(file)

# Take first 5 reviews
sample = df.head(5)

client = Groq()

reviews_text = ""

for i, (_, row) in enumerate(sample.iterrows(), start=1):
    reviews_text += f"""
REVIEW {i}
Review ID: {row['reviewId']}
App: {row['app']}
Rating: {row['rating']}
Review: {row['review_text']}
"""

prompt = f"""
You are analyzing user reviews of UPI payment applications.

Classify every review into exactly ONE topic and ONE sentiment.

TOPIC CATEGORIES:

1. Payment Failure
2. Refund Delay
3. KYC/Login
4. Fraud/Unauthorized Transaction
5. Customer Support
6. UI/Performance
7. Other

SENTIMENT:

- Positive
- Neutral
- Negative

RULES:

- Choose exactly ONE topic.
- If multiple issues exist, choose the PRIMARY issue.
- Determine sentiment from the review text, NOT the star rating.
- Do not skip any review.

Return ONLY valid JSON in this format:

[
  {{
    "review_id": "review id",
    "topic": "topic",
    "sentiment": "sentiment"
  }}
]

REVIEWS:

{reviews_text}
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)

print("=" * 70)
print("GROQ CLASSIFICATION TEST")
print("=" * 70)

print(response.choices[0].message.content)