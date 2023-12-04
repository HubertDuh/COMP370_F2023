import csv
import json
from collections import defaultdict, Counter
import argparse


def build_interaction_network(csv_file_path, json_output_path):
    interaction_counts = defaultdict(Counter)
    total_counts = Counter()

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        previous_character = None

        for row in reader:
            character = row['pony'].strip().lower()
            if any(keyword in character for keyword in ['others', 'ponies', 'all', 'and']) or character == '':
                continue
            total_counts[character] += 1
            if previous_character and previous_character != character:
                interaction_counts[previous_character][character] += 1
            previous_character = character

    top_characters = [character for character, count in total_counts.most_common(101)]
    filtered_interaction_counts = {character: counts for character, counts in interaction_counts.items() if
                                   character in top_characters}

    for character in filtered_interaction_counts:
        filtered_interaction_counts[character] = {other_character: count for other_character, count in
                                                  filtered_interaction_counts[character].items() if
                                                  other_character in top_characters}

    interaction_network = {character: dict(counts) for character, counts in filtered_interaction_counts.items()}

    with open(json_output_path, 'w') as json_file:
        json.dump(interaction_network, json_file, indent=4)


def main():
    parser = argparse.ArgumentParser(description='Build an MLP interaction network from a CSV file.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file path')
    parser.add_argument('-o', '--output', required=True, help='Output JSON file path')

    args = parser.parse_args()
    build_interaction_network(args.input, args.output)


if __name__ == "__main__":
    main()
