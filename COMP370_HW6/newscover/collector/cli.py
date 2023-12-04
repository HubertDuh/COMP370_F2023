import argparse
import json
from pathlib import Path
from newscover.newsapi import fetch_latest_news


def collect_data(api_key, keywords_dict, lookback_days, output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for key, keywords in keywords_dict.items():
        articles = fetch_latest_news(api_key, keywords, lookback_days)
        output_path = Path(output_dir) / f'{key}.json'

        with open(output_path, 'w') as output_file:
            json.dump(articles, output_file)


def main():
    parser = argparse.ArgumentParser(description='CLI tool that collects data from newsapi.org')
    parser.add_argument('-k', '--api_key', required=True, help='API key for News Api')
    parser.add_argument("-i", "--input_file", required=True, help="Input JSON file with keyword sets")
    parser.add_argument("-b", "--lookback_days", type=int, default=10, help="Number of days to look back")
    parser.add_argument("-o", "--output_dir", required=True, help="Output directory for collected data")

    args = parser.parse_args()

    with open(args.input_file, 'r') as input_file:
        keywords_dict = json.load(input_file)

    collect_data(args.api_key, keywords_dict, args.lookback_days, args.output_dir)


if __name__ == "__main__":
    main()
