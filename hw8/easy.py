# easy.py

# Prompt: Write a Python function that takes a NetworkX graph as input and returns the number of nodes in the graph.

import networkx as nx

def count_nodes(graph):
    """
    Count the number of nodes in a NetworkX graph.
    
    Parameters:
    graph (nx.Graph): The input NetworkX graph.

    Returns:
    int: The number of nodes in the graph.
    """
    return len(graph.nodes())

# Example usage
if __name__ == "__main__":
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4)])
    print(f"Number of nodes in the graph: {count_nodes(G)}")
