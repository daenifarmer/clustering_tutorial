"""Lösung Aufgabe 2: Clustergrößenverteilung n_s(p).

Berechnet n_s(p) = (Anzahl Cluster der Größe s) / L^2 am kritischen Punkt p_c
und stellt das Potenzgesetz n_s ~ s^(-tau) im doppelt-logarithmischen Plot dar.

Aufgabe 2a: n_s bei p_c für L = 200, 200 Konfigurationen.
Aufgabe 2b: Systemgrößeneinfluss – n_s für L = 50, 100, 200 im Vergleich.
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from hk import hoshen_kopelman
from gen_occupancy import gen_random_occupancy
from cluster_stats import percolating_label, cluster_sizes

matplotlib.rcParams.update({"font.size": 14})

# Kritischer Exponent und Schwellenwert für das 2D-Quadratgitter
TAU = 187 / 91   # universeller Exponent der Clustergrößenverteilung
P_C = 0.5927


def measure_ns(L, p, n_samples, rng):
    """Berechnet die gemittelte Clustergrößenverteilung n_s(p).

    Returns
    -------
    s_vals : ndarray
        Clustergrößen s (nur s > 0 mit n_s > 0).
    ns_vals : ndarray
        n_s(p) für jedes s.
    """
    all_sizes = []
    for _ in range(n_samples):
        occ = gen_random_occupancy((L, L), p, rng)
        labels, _ = hoshen_kopelman(occ)
        perc_lbl = percolating_label(labels)
        all_sizes.extend(cluster_sizes(labels, exclude_label=perc_lbl))

    if not all_sizes:
        return np.array([1.0]), np.array([0.0])

    # Histogramm: counts[s] = Anzahl Cluster der Größe s über alle Konfigurationen
    max_s = max(all_sizes)
    counts = np.zeros(max_s + 1)
    for s in all_sizes:
        counts[s] += 1

    ns = counts / (n_samples * L**2)
    s_arr = np.arange(max_s + 1, dtype=float)
    mask = (s_arr > 0) & (ns > 0)
    return s_arr[mask], ns[mask]


def fit_powerlaw(s_vals, ns_vals, s_min=5, s_max=50):
    """Fittet log(n_s) = -tau_fit * log(s) + log(C) per linearer Regression.

    Der Fit wird auf den Bereich s_min <= s <= s_max eingeschränkt.

    Returns
    -------
    tau_fit : float
        Gemessener Exponent (Steigung im Log-Log-Plot).
    C : float
        Normierungskonstante.
    s_ref : ndarray
        s-Werte für die Referenzlinie (gesamter Bereich).
    ns_ref : ndarray
        Gefittete Referenzlinie über den gesamten s-Bereich.
    """
    mask = (s_vals >= s_min) & (s_vals <= s_max)
    if mask.sum() < 3:
        mask = np.ones(len(s_vals), dtype=bool)

    # Lineare Regression: log(n_s) = slope * log(s) + intercept
    log_s = np.log(s_vals[mask])
    log_ns = np.log(ns_vals[mask])
    slope, intercept = np.polyfit(log_s, log_ns, 1)

    tau_fit = -slope
    C = np.exp(intercept)
    s_ref = np.logspace(np.log10(s_vals[0]), np.log10(s_vals[-1]), 400)
    return tau_fit, C, s_ref, C * s_ref**(-tau_fit)


# ======================================================================
# Aufgabe 2a: n_s bei p_c, L = 200, 200 Konfigurationen
# ======================================================================

if __name__ == "__main__":
    rng = np.random.default_rng(42)

    # --- Aufgabe 2a ---
    print("Aufgabe 2a: Berechne n_s(p_c) für L=200 (200 Konfigurationen) ...")
    # Für besseres Ergebnis: n_samples erhöhen
    s_200, ns_200 = measure_ns(L=200, p=P_C, n_samples=200, rng=rng)
    print(f"  Größtes Cluster: s = {int(s_200[-1])}")

    # Fit im zuverlässigen Bereich 5 <= s <= 50
    tau_fit, C_fit, s_ref, ns_ref_fit = fit_powerlaw(s_200, ns_200, s_min=5, s_max=50)
    print(f"  Gemessener Exponent:   tau_fit  = {tau_fit:.4f}")
    print(f"  Theoretischer Wert:    tau_theor = {TAU:.4f}  (= 187/91)")
    print(f"  Abweichung: {abs(tau_fit - TAU) / TAU * 100:.1f}%")

    # Theoretische Referenzlinie mit gleicher Normierung wie der Fit
    ns_ref_theor = C_fit * s_ref**(-TAU)

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.loglog(s_200, ns_200, ".", markersize=3, color="steelblue",
              label=f"$n_s$  (L=200, 200 Konf.)")
    ax.loglog(s_ref, ns_ref_fit, "-", color="orange", linewidth=2,
              label=rf"Fit: $\tau_{{fit}} = {tau_fit:.3f}$")
    ax.loglog(s_ref, ns_ref_theor, "--", color="red", linewidth=1.5,
              label=rf"Theorie: $\tau = 187/91 \approx {TAU:.3f}$")

    ax.set_xlabel("Clustergröße $s$")
    ax.set_ylabel("$n_s$")
    ax.set_title(f"Aufgabe 2a: Clustergrößenverteilung bei $p = p_c \\approx {P_C}$")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig("aufgabe2a_ns_pc.png", dpi=150)
    plt.show()
    print("  Gespeichert: aufgabe2a_ns_pc.png\n")

    # ======================================================================
    # Aufgabe 2b: Systemgrößeneinfluss – L = 50, 100, 200
    # ======================================================================
    print("Aufgabe 2b: Systemgrößeneinfluss (L = 50, 100, 200) ...")

    fig, ax = plt.subplots(figsize=(8, 6))

    for L in [50, 100, 200]:
        print(f"  L = {L} ...", end=" ", flush=True)
        if L == 200:
            s_v, ns_v = s_200, ns_200
        else:
            s_v, ns_v = measure_ns(L=L, p=P_C, n_samples=200, rng=rng)
        ax.loglog(s_v, ns_v, ".", markersize=3, label=f"L = {L}")
        print("fertig")

    # Gemeinsame theoretische Referenzgerade (Normierung aus L=200-Fit)
    ax.loglog(s_ref, ns_ref_theor, "--", color="black", linewidth=1.5,
              label=rf"$\propto s^{{-\tau}},\;\tau = {TAU:.3f}$")

    ax.set_xlabel("Clustergröße $s$")
    ax.set_ylabel("$n_s$")
    ax.set_title(f"Aufgabe 2b: Systemgrößeneinfluss auf $n_s$ bei $p = p_c$")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig("aufgabe2b_ns_systemgroesse.png", dpi=150)
    plt.show()
    print("  Gespeichert: aufgabe2b_ns_systemgroesse.png")
