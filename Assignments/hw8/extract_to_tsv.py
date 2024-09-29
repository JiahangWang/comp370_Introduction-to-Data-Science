# extract_to_tsv.py
import json
import random
import argparse


def extract_to_tsv(json_file, out_file, num_posts):

    with open(json_file, 'r') as f:
        data = json.load(f)

    posts = data['data']['children']

    num_posts = min(num_posts, len(posts))

    selected_posts = random.sample(posts, num_posts)

    with open(out_file, 'w') as f:
        f.write("Name\ttitle\tcoding\n")

        for post in selected_posts:
            name = post['data']['name']
            title = post['data']['title'].replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')
            f.write(f"{name}\t{title}\t\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract posts to TSV.')
    parser.add_argument('json_file', type=str, help='The JSON file to process')
    parser.add_argument('-o', '--out_file', type=str, help='The output TSV file')
    parser.add_argument('num_posts_to_output', type=int, help='The number of posts to output')

    args = parser.parse_args()

    extract_to_tsv(args.json_file, args.out_file, args.num_posts_to_output)
