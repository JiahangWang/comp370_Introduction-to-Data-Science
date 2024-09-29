import argparse
import json
import os
from newscover.newsapi import fetch_latest_news


def collect_news(api_key, input_file, output_dir, lookback_days=10):
    with open(input_file, 'r') as f:
        keyword_sets = json.load(f)

    for name, keywords in keyword_sets.items():
        articles = fetch_latest_news(api_key, keywords, lookback_days)
        with open(os.path.join(output_dir, f"{name}.json"), 'w') as f:
            json.dump(articles, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect news articles based on keywords.')
    parser.add_argument('-k', '--api_key', required=True, help='API key for NewsAPI')
    parser.add_argument('-b', '--lookback', type=int, default=10, help='# days to lookback')
    parser.add_argument('-i', '--input_file', required=True, help='Input JSON file containing keyword sets')
    parser.add_argument('-o', '--output_dir', required=True, help='Directory to save the collected news articles')

    args = parser.parse_args()

    collect_news(args.api_key, args.input_file, args.output_dir, args.lookback)
