"""Hilfsfunktionen zur Berechnung von Clustereigenschaften.

Dieses Modul stellt die gemeinsam genutzten Bausteine für Aufgabe 2–5 bereit:
Identifikation des perkolierenden Clusters, Clustergrößen, mittlere Clustergröße
S(p) und Dichte des perkolierenden Clusters P(p).
"""

import numpy as np


def percolating_label(labels_lattice):
    """Gibt das Label des perkolierenden Clusters zurück, oder None.

    Ein Cluster perkoliert, wenn dasselbe Label am linken und rechten Rand
    (links-rechts) oder am oberen und unteren Rand (oben-unten) auftritt.
    """
    left  = set(np.unique(labels_lattice[:, 0]))  - {0}
    right = set(np.unique(labels_lattice[:, -1])) - {0}
    spanning = left & right
    if spanning:
        return next(iter(spanning))

    top    = set(np.unique(labels_lattice[0, :]))  - {0}
    bottom = set(np.unique(labels_lattice[-1, :])) - {0}
    spanning = top & bottom
    if spanning:
        return next(iter(spanning))

    return None


def cluster_sizes(labels_lattice, exclude_label=None):
    """Gibt eine Liste der Größen aller Cluster zurück.

    Der perkolierende Cluster kann über exclude_label ausgeschlossen werden.
    """
    labels, counts = np.unique(labels_lattice, return_counts=True)
    return [
        int(c) for lbl, c in zip(labels, counts)
        if lbl != 0 and lbl != exclude_label
    ]


def mean_cluster_size(labels_lattice):
    """Berechnet die mittlere Clustergröße S(p).

    S = sum(s^2 * n_s) / sum(s * n_s), wobei der perkolierende Cluster
    ausgeschlossen wird (Aufgabe 3).
    """
    perc_lbl = percolating_label(labels_lattice)
    sizes = np.array(cluster_sizes(labels_lattice, exclude_label=perc_lbl))
    if sizes.size == 0:
        return 0.0
    return float(np.sum(sizes**2) / np.sum(sizes))


def percolating_density(labels_lattice):
    """Berechnet die Dichte des perkolierenden Clusters P(p).

    P = (Größe des perkolierenden Clusters) / (Anzahl besetzter Plätze).
    Gibt 0 zurück wenn kein perkolierender Cluster existiert (Aufgabe 4).
    """
    perc_lbl = percolating_label(labels_lattice)
    if perc_lbl is None:
        return 0.0
    n_occupied = int(np.sum(labels_lattice > 0))
    if n_occupied == 0:
        return 0.0
    return int(np.sum(labels_lattice == perc_lbl)) / n_occupied
