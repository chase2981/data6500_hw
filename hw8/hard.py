# hard.py

# Prompt: Write a Python function that takes a NetworkX graph as input and returns the number of nodes in the graph that have a degree greater than 5.

import networkx as nx

def count_high_degree_nodes(graph):
    """
    Count the number of nodes in a NetworkX graph that have a degree greater than 5.
    
    Parameters:
    graph (nx.Graph): The input NetworkX graph.

    Returns:
    int: The number of nodes with a degree greater than 5.
    """
    return sum(1 for node in graph.nodes() if graph.degree(node) > 5)

# Example usage
if __name__ == "__main__":
    G = nx.Graph()
    # Adding edges to ensure at least one node has a degree greater than 5
    G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
                      (1, 3), (2, 4), (1, 4), (2, 5), (1, 5),
                      (1, 6), (1, 7), (1, 8), (1, 9)])  # Node 1 will have degree 9
    
    print(f"Number of nodes with degree greater than 5: {count_high_degree_nodes(G)}")
