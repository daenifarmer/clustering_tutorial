"""Lösung Aufgabe 3: Mittlere Clustergröße S(p).

Berechnet S(p) = sum(s^2 * n_s) / sum(s * n_s) als Funktion der
Besetzungswahrscheinlichkeit für verschiedene Systemgrößen.
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from hk import hoshen_kopelman
from gen_occupancy import gen_random_occupancy
from cluster_stats import mean_cluster_size

matplotlib.rcParams.update({"font.size": 14})

P_C = 0.5927  # kritischer Punkt 2D-Quadratgitter


def sweep_S(L, p_values, n_samples, rng):
    """Berechnet S(p) für alle p-Werte, gemittelt über n_samples Konfigurationen.

    Parameters
    ----------
    L : int
        Seitenlänge des quadratischen Gitters.
    p_values : array_like
        Besetzungswahrscheinlichkeiten.
    n_samples : int
        Anzahl unabhängiger Konfigurationen pro p-Wert.
    rng : numpy.random.Generator

    Returns
    -------
    ndarray
        Gemittelte S(p)-Werte, eine pro Eintrag in p_values.
    """
    S_result = []
    for p in p_values:
        S_configs = []
        for _ in range(n_samples):
            occ = gen_random_occupancy((L, L), p, rng)
            labels, _ = hoshen_kopelman(occ)
            S_configs.append(mean_cluster_size(labels))
        S_result.append(np.mean(S_configs))
    return np.array(S_result)


# ======================================================================
# Aufgabe 3: S(p) für L = 32, 64, 128
# ======================================================================

if __name__ == "__main__":
    rng = np.random.default_rng(42)

    L_values  = [32, 64, 128]
    p_values  = np.arange(0.40, 0.70, 0.01)
    N_SAMPLES = 100 # mehr auch gut

    fig, ax = plt.subplots(figsize=(9, 6))

    for L in L_values:
        print(f"Aufgabe 3: Sweep S(p) für L={L} ({N_SAMPLES} Konf./p-Wert) ...",
              end=" ", flush=True)
        S = sweep_S(L, p_values, N_SAMPLES, rng)
        ax.plot(p_values, S, "o-", linewidth=1.5, markersize=4, label=f"L = {L}")
        print("fertig")

    ax.axvline(P_C, color="gray", linestyle="--", linewidth=1.2,
               label=f"$p_c \\approx {P_C}$")
    ax.set_xlabel("Besetzungswahrscheinlichkeit $p$")
    ax.set_ylabel("Mittlere Clustergröße $S(p)$")
    ax.set_title("Aufgabe 3: Mittlere Clustergröße $S(p)$")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("aufgabe3_S_vs_p.png", dpi=150)
    plt.show()
    print("Gespeichert: aufgabe3_S_vs_p.png")
