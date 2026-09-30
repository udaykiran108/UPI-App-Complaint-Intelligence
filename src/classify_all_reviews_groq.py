import pandas as pd
import json
import time
import os
from groq import Groq

INPUT_FILE = "data/processed/upi_reviews_cleaned.csv"
OUTPUT_FILE = "data/processed/upi_reviews_classified.csv"

MODEL = "openai/gpt-oss-120b"
BATCH_SIZE = 5
MAX_RETRIES = 3


# ============================================================
# LOAD INPUT DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("UPI COMPLAINT INTELLIGENCE - GROQ CLASSIFICATION")
print("=" * 70)

print(f"\nTotal reviews: {len(df)}")


# ============================================================
# LOAD OR CREATE CLASSIFICATION FILE
# ============================================================

if os.path.exists(OUTPUT_FILE):

    classified_df = pd.read_csv(OUTPUT_FILE)

    print(
        f"Existing classified file found: "
        f"{len(classified_df)} rows"
    )

else:

    classified_df = df.copy()

    classified_df["topic"] = ""

    classified_df["sentiment"] = ""

    classified_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("New classification file created.")


# Make sure classification columns are text
classified_df["topic"] = (
    classified_df["topic"]
    .fillna("")
    .astype(str)
)

classified_df["sentiment"] = (
    classified_df["sentiment"]
    .fillna("")
    .astype(str)
)


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq()


# ============================================================
# CLASSIFY ONE BATCH
# ============================================================

def classify_batch(batch):

    reviews_text = ""

    for i, (_, row) in enumerate(
        batch.iterrows(),
        start=1
    ):

        reviews_text += f"""
REVIEW {i}
Review ID: {row['reviewId']}
App: {row['app']}
Rating: {row['rating']}
Review: {row['review_text']}
"""


    prompt = f"""
You are analyzing user reviews of UPI payment applications.

Classify every review into exactly ONE topic
and ONE sentiment.

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
- Copy every Review ID EXACTLY as provided.
- Do not modify Review IDs.
- Return exactly one result for every review.

Return ONLY valid JSON.

Required format:

[
  {{
    "review_id": "EXACT_REVIEW_ID",
    "topic": "TOPIC",
    "sentiment": "SENTIMENT"
  }}
]

REVIEWS:

{reviews_text}
"""


    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


# ============================================================
# FIND REMAINING REVIEWS
# ============================================================

pending = classified_df[
    (classified_df["topic"].str.strip() == "") |
    (classified_df["sentiment"].str.strip() == "")
].copy()

print(
    f"\nReviews still needing classification: "
    f"{len(pending)}"
)


# ============================================================
# PROCESS REMAINING REVIEWS
# ============================================================

for start in range(
    0,
    len(pending),
    BATCH_SIZE
):

    batch = pending.iloc[
        start:start + BATCH_SIZE
    ]

    print("\n" + "=" * 70)

    print(
        f"Processing reviews "
        f"{start + 1} - "
        f"{start + len(batch)} "
        f"of {len(pending)}"
    )

    print("=" * 70)


    success = False


    # --------------------------------------------------------
    # RETRY SAME BATCH IF NEEDED
    # --------------------------------------------------------

    for attempt in range(
        1,
        MAX_RETRIES + 1
    ):

        try:

            print(
                f"Attempt {attempt}/{MAX_RETRIES}..."
            )

            result_text = classify_batch(batch)

            print("Response received.")


            # ------------------------------------------------
            # PARSE JSON
            # ------------------------------------------------

            results = json.loads(
                result_text
            )


            print(
                f"Groq returned "
                f"{len(results)} classifications."
            )


            # ------------------------------------------------
            # CHECK NUMBER OF RESULTS
            # ------------------------------------------------

            if len(results) != len(batch):

                print(
                    "WARNING: Wrong number of results."
                )

                if attempt < MAX_RETRIES:

                    print(
                        "Retrying this batch..."
                    )

                    time.sleep(5)

                    continue

                else:

                    print(
                        "Batch failed after retries."
                    )

                    break


            # ------------------------------------------------
            # CHECK REVIEW IDS
            # ------------------------------------------------

            expected_ids = set(
                batch["reviewId"]
                .astype(str)
            )

            returned_ids = set(
                str(item["review_id"])
                for item in results
            )


            if expected_ids != returned_ids:

                print(
                    "WARNING: Review IDs do not match."
                )

                if attempt < MAX_RETRIES:

                    print(
                        "Retrying this batch..."
                    )

                    time.sleep(5)

                    continue

                else:

                    print(
                        "Batch failed after retries."
                    )

                    break


            # ------------------------------------------------
            # VALIDATE TOPICS AND SENTIMENT
            # ------------------------------------------------

            valid_topics = {
                "Payment Failure",
                "Refund Delay",
                "KYC/Login",
                "Fraud/Unauthorized Transaction",
                "Customer Support",
                "UI/Performance",
                "Other"
            }

            valid_sentiments = {
                "Positive",
                "Neutral",
                "Negative"
            }


            valid = True


            for item in results:

                if item["topic"] not in valid_topics:

                    print(
                        f"Invalid topic: "
                        f"{item['topic']}"
                    )

                    valid = False


                if item["sentiment"] not in valid_sentiments:

                    print(
                        f"Invalid sentiment: "
                        f"{item['sentiment']}"
                    )

                    valid = False


            if not valid:

                if attempt < MAX_RETRIES:

                    print(
                        "Retrying this batch..."
                    )

                    time.sleep(5)

                    continue

                else:

                    print(
                        "Batch failed after retries."
                    )

                    break


            # ------------------------------------------------
            # SAVE RESULTS
            # ------------------------------------------------

            for item in results:

                review_id = str(
                    item["review_id"]
                )

                mask = (
                    classified_df["reviewId"]
                    .astype(str)
                    == review_id
                )

                classified_df.loc[
                    mask,
                    "topic"
                ] = str(
                    item["topic"]
                )

                classified_df.loc[
                    mask,
                    "sentiment"
                ] = str(
                    item["sentiment"]
                )


            # Save immediately
            classified_df.to_csv(
                OUTPUT_FILE,
                index=False
            )


            print(
                "Batch completed successfully."
            )

            print(
                f"Saved to: {OUTPUT_FILE}"
            )


            success = True

            break


        except json.JSONDecodeError:

            print(
                "ERROR: Groq returned invalid JSON."
            )

            if attempt < MAX_RETRIES:

                print(
                    "Retrying this batch..."
                )

                time.sleep(5)

                continue

            else:

                print(
                    "Batch failed after retries."
                )

                break


        except Exception as e:

            print(
                f"ERROR: {e}"
            )

            if attempt < MAX_RETRIES:

                print(
                    "Waiting 10 seconds before retry..."
                )

                time.sleep(10)

            else:

                print(
                    "Batch failed after retries."
                )


    # --------------------------------------------------------
    # STOP IF BATCH FAILED
    # --------------------------------------------------------

    if not success:

        print("\n" + "=" * 70)

        print(
            "CLASSIFICATION STOPPED SAFELY"
        )

        print(
            "Completed batches are already saved."
        )

        print(
            "Run the script again later to continue."
        )

        print("=" * 70)

        break


    # --------------------------------------------------------
    # WAIT BEFORE NEXT BATCH
    # --------------------------------------------------------

    print(
        "\nWaiting 5 seconds before next batch..."
    )

    time.sleep(5)


# ============================================================
# FINAL STATUS
# ============================================================

classified_df = pd.read_csv(
    OUTPUT_FILE
)


completed = (
    classified_df["topic"]
    .fillna("")
    .astype(str)
    .str.strip()
    .ne("")
    &
    classified_df["sentiment"]
    .fillna("")
    .astype(str)
    .str.strip()
    .ne("")
)


print("\n" + "=" * 70)
print("CLASSIFICATION STATUS")
print("=" * 70)

print(
    f"Total reviews: "
    f"{len(classified_df)}"
)

print(
    f"Classified reviews: "
    f"{completed.sum()}"
)

print(
    f"Remaining reviews: "
    f"{(~completed).sum()}"
)

print(
    "\nSaved file:"
)

print(
    OUTPUT_FILE
)