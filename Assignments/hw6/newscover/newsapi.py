import requests
from datetime import datetime, timedelta

def fetch_latest_news(api_key, news_keywords, lookback_days=10):
    # Calculate the date <lookback_days> ago in the required format
    lookback_date = datetime.now() - timedelta(days=lookback_days)
    lookback_date_str = lookback_date.strftime('%Y-%m-%d')

    # Construct the API URL
    base_url = 'https://newsapi.org/v2/everything'
    query = ' '.join(news_keywords)  # Combine the keywords for the query

    # Prepare the payload with parameters
    payload = {
        'q': query,
        'from': lookback_date_str,
        'language': 'en',
        'sortBy': 'publishedAt',
        'apiKey': api_key  # API key
    }

    # Make the request
    response = requests.get(base_url, params=payload)

    # Raise an exception if the request was unsuccessful
    response.raise_for_status()

    # Parse the response assuming the content is in JSON format
    results = response.json()

    # Extract the articles from the results
    articles = results['articles']

    return articles

# Test the function
if __name__ == "__main__":
    api_key = "6bb1ec6c02db4535b7f67891a2d9d6af"
    test_keywords = ["technology", "AI"]  # Example keywords
    try:
        articles = fetch_latest_news(api_key, test_keywords)
        for article in articles:
            print(article['title'])  # Print the title of each article
    except Exception as e:
        print(f"An error occurred: {e}")
