import argparse
import json
import math
from collections import defaultdict, Counter

def read_pony_counts(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def compute_tfidf(pony_counts, num_words):
    total_ponies = len(pony_counts)
    word_pony_usage = Counter()

    # Calculate the number of ponies that use each word
    for pony in pony_counts:
        for word in pony_counts[pony]:
            word_pony_usage[word] += 1

    # Compute TF-IDF for each word for each pony
    tfidf_scores = defaultdict(dict)
    for pony, words in pony_counts.items():
        for word, count in words.items():
            tf = count
            idf = math.log(total_ponies / word_pony_usage[word])
            tfidf_scores[pony][word] = tf * idf

    # Select top words based on TF-IDF scores
    top_words = {pony: sorted(words, key=words.get, reverse=True)[:num_words] for pony, words in tfidf_scores.items()}

    return top_words

def main(pony_counts_file, num_words):
    pony_counts = read_pony_counts(pony_counts_file)
    top_words = compute_tfidf(pony_counts, num_words)
    print(json.dumps(top_words, indent=4))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compute top TF-IDF words for each MLP character.')
    parser.add_argument('-c', '--counts', required=True, help='Path to the pony_counts.json file')
    parser.add_argument('-n', '--numwords', required=True, type=int, help='Number of top words to output for each pony')
    args = parser.parse_args()

    main(args.counts, args.numwords)
