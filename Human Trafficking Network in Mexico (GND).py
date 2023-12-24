""" Generalized Network Dismantling (GND) algorithm
Collective Interactions of a Human Trafficking Network in Mexico and the Limits of Dismantling Strategies """

# Import libraries
import networkx as nx
from networkx.algorithms.approximation import min_weighted_vertex_cover
from scipy.sparse.linalg import eigsh
from scipy.sparse import diags
import numpy as np
import time

def CM(G):
    """
    Compute the length of the largest connected component of the network.
    :param G: NetworkX Graph
    :return: Integer representing the number of nodes in the largest connected component of G
    """
    if len(G) == 0:
        return 0
    return max(len(n) for n in nx.connected_components(G))

def removal(G, v, disman):
    """
    Remove a node and update the dismantling summary.
    :param G: NetworkX Graph
    :param v: Node to remove
    :param disman: Dictionary to update with removal cost, node id, and size of largest connected component
    """
    G.graph['cost'] += G.degree(v)
    G.remove_node(v)
    disman['Cost'] = str(G.graph['cost'])
    disman['Node_id'] = v
    disman['Size_LCC'] = int(CM(G))
    print(disman)

def GND(G):
    """
    Execute the Generalized Network Dismantling algorithm on a given graph.
    :param G: NetworkX Graph
    :return: Dictionary table showing the data of aggregate cost of removal, size of the largest 
             component of the network G, and iteration
    """
    disman = {}
    while CM(G) > 2:  # While the largest component is greater than the threshold C do:
        cmm = G.subgraph(max(nx.connected_components(G), key=len))  # Largest connected component
        index = {k: i for i, k in enumerate(list(cmm.nodes()))}

        A = nx.adjacency_matrix(cmm)  # Adjacency matrix of the largest component
        W = diags([w for v, w in cmm.degree()])  # Weight matrix based on the degrees of each node
        B = A * W + W * A - A
        DB = diags(np.squeeze(np.asarray(B.sum(axis=1))), dtype=np.int32)  # Diagonal degree matrix
        L = DB - B  # Laplacian matrix of the largest component

        itera = 100 * L.shape[0]
        eigen_values, eigen_vectors = eigsh(L.astype(np.float32), k=2, which='SM', maxiter=itera)
        Fielder_vector = eigen_vectors[:, 1]

        G_star = nx.Graph()
        for i, j in cmm.edges():
            if Fielder_vector[index[i]] * Fielder_vector[index[j]] <= 0:
                G_star.add_edge(i, j)

        for v in G_star.nodes():
            G_star.nodes[v]["weight"] = 1.0 / G_star.degree(v)

        cover = list(min_weighted_vertex_cover(G_star, weight='weight'))
        cover.sort(key=cmm.degree())

        for node in cover:
            removal(G, node, disman)

    for node in [node for i, node in G.edges()]:
        removal(G, node, disman)

    for node in list(G.nodes()):
        removal(G, node, disman)

network = "Data.txt"  # File with nodes and edges
Net = nx.read_edgelist(network)  # NetworkX Graph for the network
Net.graph['cost'] = 0  # Start with cost zero of removal cause is the complete network
GND(Net)