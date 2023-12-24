"""
Human Capital Disruption Algorithm from Human and Social Capital Strategies for Mafia Network Disruption. 
"""

# Import libraries
import networkx as nx
import pandas as pd
import numpy as np

def calculate_degree_centrality(G, nodes):
    """
    Calculate the degree centrality for nodes in a graph
    :param G: NetworkX graph
    :param nodes: nodes for which to calculate centrality
    :return: dictionary of nodes with their degree centrality
    """
    centrality = nx.degree_centrality(G)
    return {node: centrality[node] for node in nodes}

def human_capital_disruption(G, labels):
    """
    Implement the Human Capital Disruption algorithm on a graph.
    :param G: NetworkX graph
    :param labels: target labels for disruption
    :return: normalized metrics of connected components, largest connected component, and global efficiency
    """
    # Initial metrics
    cc0 = nx.number_connected_components(G)
    lcc0 = len(max(nx.connected_components(G), key=len))
    E0_glob = nx.global_efficiency(G)
    S = {n for n, attr in G.nodes(data=True) if attr['label'] in labels}
    T = len(S)
    ccs, lccs, E_glob = [], [], []

    for s in range(1, T + 1):
        centrality = calculate_degree_centrality(G, S)
        c = max(centrality, key=centrality.get)
        S.remove(c)
        G.remove_node(c)
        current_cc = nx.number_connected_components(G) / cc0
        current_lcc = len(max(nx.connected_components(G), key=len)) / lcc0
        current_E_glob = nx.global_efficiency(G) / E0_glob
        ccs.append(current_cc)
        lccs.append(current_lcc)
        E_glob.append(current_E_glob)

    return ccs, lccs, E_glob

def load_graph(edges_file):
    """
    Load a graph from an edge list file.
    :param edges_file: path to file
    :return: NetworkX graph
    """
    G = nx.Graph()
    with open(edges_file, 'r') as file:
        for line in file:
            node1, node2 = map(int, line.strip().split())
            G.add_edge(node1, node2)
    return G

def load_labels(csv_file, G):
    """
    Load node labels from a CSV file and assign to the graph.
    :param csv_file: path to CSV file
    :param G: NetworkX graph
    """
    labels_df = pd.read_csv(csv_file, header=None)
    for index, row in labels_df.iterrows():
        node = int(row[0])
        label = row[1].split()[0].lower()  # Taking only the first word of the label
        if node in G:
            G.nodes[node]['label'] = label

def calculate_fragmentation(G):
    """
    Calculate the exact fragmentation of a graph.
    :param G: NetworkX graph
    :return: fragmentation value
    """
    n = len(G)
    adjacency_matrix = nx.adjacency_matrix(G).todense()
    disconnected_pairs = np.sum(np.logical_not(adjacency_matrix)) / 2
    total_pairs = n * (n - 1) / 2
    fragmentation = 1 - disconnected_pairs / total_pairs
    return fragmentation

def calculate_network_betweenness_centrality(G):
    """
    Calculate the network-wide betweenness centrality.
    :param G: NetworkX graph
    :return: network betweenness centrality value
    """
    node_betweenness = nx.betweenness_centrality(G)
    total_betweenness = sum(node_betweenness.values())
    n = G.number_of_nodes()
    max_possible_betweenness = (n-1)*(n-2)/2
    network_betweenness_centrality = total_betweenness / max_possible_betweenness
    return network_betweenness_centrality

def compute_additional_metrics(G):
    """
    Compute additional metrics for a given graph.
    :param G: NetworkX graph
    :return: dictionary of metrics including betweenness centrality, average clustering coefficient, and more
    """
    metrics = {}
    metrics['betweenness_centrality'] = calculate_network_betweenness_centrality(G)
    metrics['average_clustering_coefficient'] = nx.average_clustering(G)
    metrics['density'] = nx.density(G)
    metrics['fragmentation'] = calculate_fragmentation(G)
    if nx.is_connected(G):
        metrics['diameter'] = nx.diameter(G)
    else:
        metrics['diameter'] = float('inf')
    degree_dict = dict(G.degree())
    metrics['average_degree'] = sum(degree_dict.values()) / float(G.number_of_nodes())
    return metrics

# Load data
edges_file = 'Data.txt'  
labels_file = 'labels.csv' 

G = load_graph(edges_file)
load_labels(labels_file, G)

labels = ["ciudador", "reclutador", "victima-reclutador"]
ccs, lccs, E_glob = human_capital_disruption(G, labels)

additional_metrics = compute_additional_metrics(G)

print("Normalized number of connected components:", ccs)
print("Normalized size of the largest connected component:", lccs)
print("Normalized average global efficiency:", E_glob)
print("Additional Metrics:")
for metric, value in additional_metrics.items():
    print(f"{metric}: {value}")