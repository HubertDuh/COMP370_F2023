import requests
from bs4 import BeautifulSoup
import json
import argparse
from pathlib import Path

CACHE_FILE = "cache_homepage.html"
CACHE_DIR = Path("cache_files")
TRENDING_ARTICLES_COUNT = 5

CACHE_DIR.mkdir(exist_ok=True)


def fetch_html(url, cache_file=None):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'}

    if cache_file and cache_file.exists():
        return cache_file.read_text(encoding='utf-8')

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL {url}. Status code: {response.status_code}")

    html_content = response.text

    if cache_file:
        cache_file.write_text(html_content, encoding='utf-8')

    return html_content


def get_trending_links(homepage_html):
    soup = BeautifulSoup(homepage_html, 'html.parser')
    article_elements = soup.select(
        ".list-widget-trending ol.list-widget__content li[data-carousel-item] article")

    urls = []

    for article in article_elements:
        data = json.loads(article.attrs.get('data-evt-val', '{}'))
        url = data.get('target_url')
        if url:
            urls.append(url)

    return urls[:TRENDING_ARTICLES_COUNT]


def extract_article_data(article_url):
    cache_path = CACHE_DIR / (article_url.split('/')[-2] + ".html")
    html_content = fetch_html(article_url, cache_file=cache_path)

    soup = BeautifulSoup(html_content, 'html.parser')

    title_element = soup.select_one(".article-title")
    title = title_element.text.strip() if title_element else ""

    publication_date_element = soup.select_one(
        ".published-date .published-date__since")
    publication_date = publication_date_element.text.replace(
        "Published ", "").strip() if publication_date_element else ""

    author_element = soup.select_one(".published-by .published-by__author a")
    author = author_element.text.strip() if author_element else ""

    blurb_element = soup.select_one(".article-subtitle")
    blurb = blurb_element.text.strip() if blurb_element else ""

    return {
        "title": title,
        "publication_date": publication_date,
        "author": author,
        "blurb": blurb
    }


def main(output_file):
    cache_path_homepage = CACHE_DIR / CACHE_FILE
    homepage_html = fetch_html(
        "https://montrealgazette.com/category/news/", cache_file=cache_path_homepage)
    trending_links = get_trending_links(homepage_html)

    trending_data = []
    for link in trending_links:
        data = extract_article_data(link)
        trending_data.append(data)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(trending_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Scrape trending articles from Montreal Gazette.')
    parser.add_argument('-o', '--output', required=True,
                        help='Output JSON file')
    args = parser.parse_args()
    main(args.output)
