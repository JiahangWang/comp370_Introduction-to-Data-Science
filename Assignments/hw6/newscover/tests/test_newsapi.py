import unittest
from unittest.mock import patch
import datetime
from newscover.newsapi import fetch_latest_news


class TestFetchLatestNews(unittest.TestCase):

    def setUp(self):
        self.api_key = '6bb1ec6c02db4535b7f67891a2d9d6af'

        self.mock_response_success = {
            'status': 'ok',
            'articles': [{
                'source': {
                    'id': 'techcrunch',
                    'name': 'TechCrunch'
                },
                'author': 'John Doe',
                'title': 'Amazing Developments in AI!',
                'description': 'A detailed look into the recent advancements in artificial intelligence.',
                'url': 'https://example.com/ai-news',
                'urlToImage': 'https://example.com/images/ai-news.jpg',
                'publishedAt': '2023-10-07T04:00:00Z',
                'content': 'The world of AI has seen tremendous growth in the past year. With developments in neural networks and machine learning algorithms, the capabilities of AI systems have expanded exponentially...'
            }]
        }

    @patch('newscover.newsapi.requests.get')
    def test_no_keywords(self, mock_get):
        """Test if fetch_latest_news fails when no news_keywords are provided."""
        # Set the expected error return for the API call
        mock_response_error = {'status': 'error', 'message': 'Keywords are missing'}
        mock_get.return_value.json.return_value = mock_response_error

        # We expect the function to raise an exception because no keywords were provided.
        with self.assertRaises(Exception):
            fetch_latest_news(self.api_key, [])

    @patch('newscover.newsapi.requests.get')
    def test_lookback_days(self, mock_get):
        """Test if lookback_days correctly restricts the date range of the returned news articles."""
        mock_get.return_value.json.return_value = self.mock_response_success

        # Assuming today's date is 2023-10-10, for the purpose of the test, we look back 7 days
        lookback_days = 7
        today = datetime.datetime(2023, 10, 10)
        past_date_limit = today - datetime.timedelta(days=lookback_days)

        articles = fetch_latest_news(self.api_key, ['test'], lookback_days=lookback_days)

        for article in articles:
            published_date = datetime.datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            # If the publication date is before the past date limit, then the test fails.
            self.assertTrue(published_date > past_date_limit)

    @patch('newscover.newsapi.requests.get')
    def test_invalid_keyword(self, mock_get):
        """Test if fetch_latest_news fails when a keyword contains non-alphabetical characters."""
        # Set the expected error return for the API call
        mock_response_error = {'status': 'error', 'message': 'Invalid keyword'}
        mock_get.return_value.json.return_value = mock_response_error

        invalid_keyword = 'inv@lid'  # Keyword includes non-alphabetical character

        # We expect the function to raise an exception because an invalid keyword was provided.
        with self.assertRaises(Exception):
            fetch_latest_news(self.api_key, [invalid_keyword])


if __name__ == '__main__':
    unittest.main()
