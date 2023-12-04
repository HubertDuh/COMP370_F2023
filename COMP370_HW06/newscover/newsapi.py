import requests
import datetime
import os

NEWS_API_URL = "https://newsapi.org/v2/everything"


def fetch_latest_news(api_key, news_keywords, lookback_days=10):
    for word in news_keywords:
        if not word.isalpha():
            raise ValueError('Keywords must only contain alphabetic characters.')

    date = (datetime.date.today() - datetime.timedelta(lookback_days))

    params = {
        'apiKey': api_key,
        'q': 'AND'.join(news_keywords),
        'from': date,
        'language': 'en',
        'sortBy': 'publishedAt',
    }

    response = requests.get(NEWS_API_URL, params=params)

    if response.status_code == 200:
        articles = response.json().get('articles', [])

        clean_articles = []

        for artic in articles:
            if artic['content'] != "[Removed]":
                clean_articles.append(artic)

        return clean_articles
    else:
        raise ValueError(f'Error response code {response.status_code}: {response.text}')


if __name__ == "__main__":
    api_key = os.environ.get('API_KEY')
    news_keywords = ["taylor", "swift"]

    latest_news = fetch_latest_news(api_key, news_keywords)

    for article in latest_news:
        print(article['title'])
