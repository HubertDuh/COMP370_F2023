import json
import random
import argparse
import csv


def extract_posts(json_file, num_of_posts):
    with open(json_file, 'r') as file:
        data = json.load(file)
        posts = data['data']['children']
        if num_of_posts > len(posts):
            return posts
        else:
            return random.sample(posts, num_of_posts)


def write_to_tsv(posts, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(['Name', 'Title', 'Coding'])
        for post in posts:
            name = post['data']['name']
            title = post['data']['title'].replace('\n', ' ').replace('\r', ' ')
            writer.writerow([name, title, ''])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output_file', required=True, help='Output TSV file')
    parser.add_argument('json_file', help='Input JSON file')
    parser.add_argument('num_posts', type=int, help='Number of posts to output')
    args = parser.parse_args()

    posts = extract_posts(args.json_file, args.num_posts)
    write_to_tsv(posts, args.output_file)


if __name__ == '__main__':
    main()
