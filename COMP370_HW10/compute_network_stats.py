import json
import networkx as nx
from operator import itemgetter
import argparse
import matplotlib.pyplot as plt


def compute_network_stats(input_json_path, output_json_path):
    with open(input_json_path, 'r') as file:
        interaction_network = json.load(file)

    G = nx.Graph()
    for character, interactions in interaction_network.items():
        for other_character, weight in interactions.items():
            G.add_edge(character, other_character, weight=weight)

    visualize_network(G)

    degree_centrality = nx.degree_centrality(G)
    weighted_degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)

    top_degree = sorted(degree_centrality.items(), key=itemgetter(1), reverse=True)[:3]
    top_weighted_degree = sorted(weighted_degree_centrality.items(), key=itemgetter(1), reverse=True)[:3]
    top_closeness = sorted(closeness_centrality.items(), key=itemgetter(1), reverse=True)[:3]
    top_betweenness = sorted(betweenness_centrality.items(), key=itemgetter(1), reverse=True)[:3]

    stats = {
        'degree': [character for character, _ in top_degree],
        'weighted_degree': [character for character, _ in top_weighted_degree],
        'closeness': [character for character, _ in top_closeness],
        'betweenness': [character for character, _ in top_betweenness]
    }

    with open(output_json_path, 'w') as file:
        json.dump(stats, file, indent=4)


def visualize_network(G):
    pos = nx.circular_layout(G)

    nx.draw_networkx_nodes(G, pos, node_color='lightblue', edgecolors='black')
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)

    plt.axis('off')
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Compute network statistics.')
    parser.add_argument('-i', '--input', required=True, help='Input JSON file path')
    parser.add_argument('-o', '--output', required=True, help='Output JSON file path')

    args = parser.parse_args()

    compute_network_stats(args.input, args.output)


if __name__ == '__main__':
    main()
