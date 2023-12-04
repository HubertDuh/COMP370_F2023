import argparse
import json
import math
from collections import defaultdict

def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", required=True, help="Pony counts JSON file path")
    parser.add_argument("-n", type=int, required=True, help="Number of top words")
    args = parser.parse_args()

    # Read the JSON file
    with open(args.c, 'r') as file:
        pony_counts = json.load(file)

    # Calculate IDF values
    total_ponies = len(pony_counts)
    word_pony_counts = defaultdict(int)
    for pony, words in pony_counts.items():
        for word in words:
            word_pony_counts[word] += 1

    idf = {word: math.log(total_ponies / count) for word, count in word_pony_counts.items()}

    # Compute TF-IDF scores and find top words
    top_words = {}
    for pony, words in pony_counts.items():
        tf_idf_scores = {word: count * idf[word] for word, count in words.items()}
        sorted_words = sorted(tf_idf_scores, key=tf_idf_scores.get, reverse=True)
        top_words[pony] = sorted_words[:args.n]

    # Save the result to distinctive_pony_words.json
    with open('distinctive_pony_words.json', 'w') as output_file:
        json.dump(top_words, output_file, indent=4)

if __name__ == "__main__":
    main()
