"""Cluster merging utilities using union-find data structure.

This module provides functions to merge cluster labels that belong to
the same connected component, using NetworkX's UnionFind implementation.
"""

import matplotlib.pyplot as plt
import networkx as nx
from union_find import UnionFind


def draw_cluster_identities(unique_labels, to_be_merged, fname=None):
    """Visualize cluster identity relationships as a graph.

    Creates a graph where nodes are cluster labels and edges connect
    labels that need to be merged.

    Parameters
    ----------
    unique_labels : iterable
        Collection of all unique cluster labels.
    to_be_merged : list of tuple
        List of (label1, label2) pairs indicating labels to merge.
    fname : str, optional
        If provided, saves the figure to this filename.
    """
    G = nx.Graph()
    G.add_nodes_from(unique_labels)
    G.add_edges_from(to_be_merged)

    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, with_labels=True)
    if fname:
        plt.savefig(fname)
    plt.show()


def get_representative_labels(unique_labels, to_be_merged):
    """Compute representative labels for each cluster using union-find.

    Processes merge requests and returns a mapping from each original
    label to its representative (canonical) label in the merged cluster.

    Parameters
    ----------
    unique_labels : iterable
        Collection of all unique cluster labels.
    to_be_merged : list of tuple
        List of (label1, label2) pairs indicating labels to merge.

    Returns
    -------
    dict
        Mapping from each label to its representative label.
    """
    uf = UnionFind(unique_labels)

    for u, v in to_be_merged:
        uf.union(u, v)

    return {l: uf.find(l) for l in unique_labels}

if __name__ == "__main__":
    print("=== Cluster Merging Demo (Union-Find) ===\n")

    unique_labels = [1, 2, 3, 4, 5, 6,7]
    to_be_merged = [(1, 2), (2, 3), (2, 4), (5, 6),(3,7)]

    print(f"Initial labels: {unique_labels}")
    print(f"Merge operations: {to_be_merged}")
    print("  1-2, 3-4, 2-3 form one component; 5-6 form another")

    print("\nGenerating cluster identity graph...")
    draw_cluster_identities(unique_labels, to_be_merged, fname="cluster_identity_graph.png")

    representative_labels = get_representative_labels(unique_labels, to_be_merged)
    print(f"\nFinal representative labels: {set(representative_labels.values())}")
    print(f"Full mapping: {representative_labels}")

