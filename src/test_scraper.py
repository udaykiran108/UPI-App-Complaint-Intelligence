from google_play_scraper import reviews, Sort

result, continuation_token = reviews(
    "com.phonepe.app",
    lang="en",
    country="in",
    sort=Sort.NEWEST,
    count=10
)

print("Number of reviews:", len(result))

for review in result:
    print(review["content"])