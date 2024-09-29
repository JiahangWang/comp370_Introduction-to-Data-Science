import requests
import pandas as pd
from datetime import datetime, timedelta

# Initialize variables
base_url = "https://gnews.io/api/v4/search"
api_key = "8950b8a71ee6bd459b80b0b0e8251159"  # Replace with your GNews API key
start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')  # Set the start date to 30 days ago
end_date = datetime.now().strftime('%Y-%m-%d')  # Set the end date to today
news_data = []

# Loop through each page of data
page = 1
while True:
    params = {
        "q": "Taylor Swift",
        "country": ["US", "CA"],
        "token": api_key,
        "lang": "en",
        "max": 10,  # Maximum of 10 news articles per request
        "from": start_date,
        "to": end_date,
        "page": page  # Set the current page number
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        break  # Exit loop if the request fails

    articles = response.json().get("articles", [])
    if not articles:
        break  # Exit loop if there are no more articles

    # Filter for news containing "Taylor Swift"
    for article in articles:
        if "Taylor Swift" in article["title"] or "Taylor Swift" in article["description"]:
            news_data.append(article)

    page += 1  # Increment the page number to fetch the next page of data

# Save to a CSV file
df = pd.DataFrame(news_data)
df.to_csv("taylor_swift_news.csv", index=False)
