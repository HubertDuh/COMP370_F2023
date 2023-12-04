import unittest
import datetime
from newscover.newsapi import fetch_latest_news
import os

API_KEY = os.environ.get('API_KEY')


class NewsAPITest(unittest.TestCase):

    def test_no_keywords(self):
        with self.assertRaises(ValueError):
            fetch_latest_news(API_KEY, news_keywords=[])

    def test_lookback_days(self):
        news_keywords = ['technology']
        lookback_days = 5

        latest_news = fetch_latest_news(API_KEY, news_keywords, lookback_days)

        for article in latest_news:
            published_at = ((datetime.datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'))
                            )
            days_difference = (datetime.datetime.today() - published_at).days
            self.assertLessEqual(days_difference, lookback_days)

    def test_wrong_keyword_test(self):
        news_keywords = ['tech#ology']

        with self.assertRaises(ValueError):
            fetch_latest_news(API_KEY, news_keywords)


if __name__ == '__main__':
    unittest.main()