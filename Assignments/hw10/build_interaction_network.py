import pandas as pd
import json
import argparse
from collections import defaultdict, Counter

def is_valid_character(name, excluded_keywords):
    return all(keyword not in name.lower() for keyword in excluded_keywords)

def main(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Convert character names to lowercase
    df['pony'] = df['pony'].str.lower()

    # Filter out invalid characters and find top 101 characters
    excluded_keywords = ["others", "ponies", "and", "all"]
    valid_characters = df['pony'][df['pony'].apply(is_valid_character, args=(excluded_keywords,))]
    top_characters = Counter(valid_characters).most_common(101)

    # Build the interaction network
    interaction_network = defaultdict(lambda: defaultdict(int))
    last_speaker = None
    last_episode = None

    for _, row in df.iterrows():
        current_speaker = row['pony']
        current_episode = row['title']

        # Check if the speaker is valid and if the episode has changed
        if current_speaker in dict(top_characters) and is_valid_character(current_speaker, excluded_keywords):
            if last_speaker and last_speaker != current_speaker and last_episode == current_episode:
                interaction_network[last_speaker][current_speaker] += 1

            last_speaker = current_speaker
        else:
            last_speaker = None

        last_episode = current_episode

    # Sort the interactions for each character
    sorted_interaction_network = {}
    for speaker, interactions in interaction_network.items():
        sorted_interactions = sorted(interactions.items(), key=lambda x: x[1], reverse=True)
        sorted_interaction_network[speaker] = dict(sorted_interactions)

    # Write to JSON
    with open(output_file, 'w') as file:
        json.dump(sorted_interaction_network, file, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Interaction Network from My Little Pony Dialogues")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file path")
    parser.add_argument("-o", "--output", required=True, help="Output JSON file path")
    args = parser.parse_args()

    main(args.input, args.output)
