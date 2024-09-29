import argparse
import csv
import json
import os
import string
from collections import defaultdict, Counter


def read_stopwords(file_path):
    with open(file_path, 'r') as file:
        stopwords = set(file.read().splitlines())
    return stopwords


def process_text(text, stopwords):
    # Replace punctuation with spaces and split into words
    for punc in string.punctuation:
        text = text.replace(punc, ' ')
    words = text.lower().split()

    # Filter out non-alphabetic words and stopwords
    return [word for word in words if word.isalpha() and word not in stopwords]


def main(dialog_file, output_file, stopwords_file):
    # Read stopwords
    stopwords = read_stopwords(stopwords_file)

    # Valid pony names
    valid_ponies = {"twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"}

    # Initialize word count dictionary for each pony
    pony_word_counts = defaultdict(Counter)

    # Process dialog file
    with open(dialog_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pony = row['pony'].lower()
            if pony in valid_ponies:
                words = process_text(row['dialog'], stopwords)
                for word in words:
                    pony_word_counts[pony][word] += 1

    # Filter out words from each pony's count that do not meet the frequency threshold of 5
    final_word_counts = {
        pony: {word: count for word, count in counts.items() if count >= 5}
        for pony, counts in pony_word_counts.items()
    }

    # Create directories if they don't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write output to JSON file
    with open(output_file, 'w') as outfile:
        json.dump(final_word_counts, outfile, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compile word counts for MLP characters.')
    parser.add_argument('-d', '--dialog', required=True, help='Path to the clean_dialog.csv file')
    parser.add_argument('-o', '--output', required=True, help='Output JSON file path')
    parser.add_argument('-s', '--stopwords', required=True, help='Path to the stopwords.txt file')
    args = parser.parse_args()

    main(args.dialog, args.output, args.stopwords)
