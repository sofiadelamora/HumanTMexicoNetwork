# Generalized Network Dismantling (GND) algorithm
# Collective Interactions of a Human Trafficking Network in Mexico and the Limits of Dismantling Strategies

# Import libraries
import networkx as nx
from networkx.algorithms.approximation import min_weighted_vertex_cover
from scipy.sparse.linalg import eigsh
from scipy.sparse import diags
import numpy as np
import time

start_time = time.time() # Start time for knowing algorithms elapsed time at end

def  CM (G):
    # This function computes the len of the biggest connected component of the network
    # Input: 
    ## G: NetworkX Graph
    # Output: number of nodes in G
    if len(G) == 0:
        return 0
    return max([len(n) for n in nx.connected_components(G)])

def removal(G,v, disman):
    lis = []
    # Removes the node indicated and adds the corresponding cost
    # Input:
    ## G: NetworkX Graph
    ## v: node to remode
    # Output:
    ## Agregated ost of node removal
    ## Number of node v
    ## Size of the biggest connected component
    G.graph['cost'] += G.degree(v)
    G.remove_node(v)
    disman['Cost'] = str(G.graph['cost'])
    disman['Node_id'] = v
    disman['Size_LCC'] =  int(CM(G))
    print(disman)

def GND(G):
    # Compute GND algorithm
    # Input:
    ## G: NetworkX Graph
    # Output: 
    ## disman: dictonary table shows the data of aggregate cost of removal, size of the largest 
    ## component of the network G and iteration
    
    disman={}
    while CM(G) > 2: #While the largest component is greater than the threshold C do:
        # Compute the partition of the largest connected component (LCC):
        cmm = G.subgraph(max(nx.connected_components(G), key=len)) #Largest connected component
        index =  {k:i for i,k in enumerate(list(cmm.nodes()))}

        # Matrixes to obtain spectral properties:
        A = nx.adjacency_matrix(cmm) # Adjacency matrix of the largest component
        W = diags([w for v, w in cmm.degree()]) # Weight matrix based on the degrees of each node
        B = A * W + W * A - A 
        DB = diags(np.squeeze(np.asarray(B.sum(axis=1))),dtype=np.int32) # Matrix for the optimization problem
        L = DB - B # Laplacian matrix of the largest component

        # Get Spectral Properties:
        itera = 100 *L.shape[0]
        eigen_values, eigen_vectors = eigsh(L.astype(np.float32),k=2,which='SM',maxiter= itera)
        Fielder_vector = eigen_vectors[:,1]

        #Subnetwork G*
        G_star = nx.Graph()
        for i,j in cmm.edges(): # We add to the subnet the edges joining nodes with different signs
            if Fielder_vector[index[i]]*Fielder_vector[index[j]] <= 0:
                G_star.add_edge(i,j)

        # Weighted Vertex Coverage:
        for v in G_star.nodes(): # Removal cost
            G_star.nodes[v]["weight"] = 1.0 / G_star.degree(v)

        cover = list(min_weighted_vertex_cover(G_star, weight='weight')) 
        cover.sort(key=cmm.degree())

        # Remove nodes in the network cover
        for node in cover:
            removal(G,node, disman)
            
    # Delete the rest of the unneeded nodes
    ## Nodes that can be trivially removed
    ## Nodes left with only one connection
    for node in [node for i,node in G.edges()]: # Nodes with only one connection
        removal(G,node, disman)
        
    # Nodes that are isolated
    for node in list(G.nodes()): # Remove isolated nodes
        removal(G,node, disman)

network = "Data.txt" # File with nodes and edges
Net = nx.read_edgelist(network) # NetworkX Graph for the network
Net.graph['cost'] = 0 #Start with cost zero of removal cause is the complete network
GND(Net)