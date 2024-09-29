import json
import argparse
import networkx as nx
from operator import itemgetter

def compute_top_n_centrality(graph, centrality_func, top_n):
    centrality = centrality_func(graph)
    sorted_centrality = sorted(centrality.items(), key=itemgetter(1), reverse=True)
    return sorted_centrality[:top_n]

def compute_weighted_degree_centrality(graph, top_n):
    centrality = {}
    for node in graph:
        centrality[node] = sum(weight for _, _, weight in graph.edges(node, data='weight'))
    return sorted(centrality.items(), key=itemgetter(1), reverse=True)[:top_n]

def main(input_file, output_file, top_n):
    # Read the interaction network JSON file
    with open(input_file, 'r') as file:
        interaction_network = json.load(file)

    # Create a graph from the interaction network
    G = nx.Graph()
    for character, interactions in interaction_network.items():
        for other_character, weight in interactions.items():
            G.add_edge(character, other_character, weight=weight)

    # Compute centralities
    degree = compute_top_n_centrality(G, nx.degree_centrality, top_n)
    weighted_degree = compute_weighted_degree_centrality(G, top_n)
    closeness = compute_top_n_centrality(G, nx.closeness_centrality, top_n)
    betweenness = compute_top_n_centrality(G, nx.betweenness_centrality, top_n)

    # Write the results to the output JSON file
    stats = {
        "degree": [character for character, _ in degree],
        "weighted_degree": [character for character, _ in weighted_degree],
        "closeness": [character for character, _ in closeness],
        "betweenness": [character for character, _ in betweenness]
    }
    with open(output_file, 'w') as file:
        json.dump(stats, file, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute Network Statistics")
    parser.add_argument("-i", "--input", required=True, help="Input JSON file path")
    parser.add_argument("-o", "--output", required=True, help="Output JSON file path")
    parser.add_argument("-n", "--top_n", type=int, default=3, help="Number of top characters to find")
    args = parser.parse_args()

    main(args.input, args.output, args.top_n)
