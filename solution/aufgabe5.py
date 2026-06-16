"""Lösung Aufgabe 5 (Bonus): Bestimmung des kritischen Punkts p_c.

Schätzt p_c aus den Plots von S(p) und P(p):

Aufgabe 5a: Peak-Position von S(p) als Schätzer für p_c.
    Das Maximum von S(p) liegt bei endlichem L leicht oberhalb von p_c.
    Mit wachsendem L konvergiert es gegen p_c.

Aufgabe 5b: Schnittpunkt der P(p)-Kurven verschiedener Systemgrößen.
    Die Kurven P(p, L) schneiden sich nahe p_c, da P(p_c, L) schwach
    L-abhängig ist.

Beide Observablen werden in einem gemeinsamen Sweep berechnet,
um doppelte Rechenzeit zu vermeiden.
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from hk import hoshen_kopelman
from gen_occupancy import gen_random_occupancy
from cluster_stats import mean_cluster_size, percolating_density

matplotlib.rcParams.update({"font.size": 14})

P_C_THEORIE = 0.5927  # theoretischer kritischer Punkt 2D-Quadratgitter


def sweep_S_and_P(L, p_values, n_samples, rng):
    """Berechnet S(p) und P(p) gleichzeitig für alle p-Werte.

    S und P werden aus derselben Konfiguration gelesen, um Rechenzeit zu sparen.

    Returns
    -------
    S_vals, P_vals : ndarray
        Gemittelte S(p)- und P(p)-Werte.
    """
    S_result, P_result = [], []
    for p in p_values:
        S_configs, P_configs = [], []
        for _ in range(n_samples):
            occ = gen_random_occupancy((L, L), p, rng)
            labels, _ = hoshen_kopelman(occ)
            S_configs.append(mean_cluster_size(labels))
            P_configs.append(percolating_density(labels))
        S_result.append(np.mean(S_configs))
        P_result.append(np.mean(P_configs))
    return np.array(S_result), np.array(P_result)


def find_crossing(p_values, curve_small_L, curve_large_L):
    """Findet den Schnittpunkt zweier P(p)-Kurven durch lineare Interpolation.

    Unterhalb p_c gilt P(L_klein) > P(L_gross); oberhalb umgekehrt.
    Der Vorzeichenwechsel der Differenz gibt den Schnittpunkt.

    Returns
    -------
    float or None
        Interpolierter p-Wert am Schnittpunkt, oder None falls nicht gefunden.
    """
    diff = curve_small_L - curve_large_L
    sign_changes = np.where(np.diff(np.sign(diff)))[0]
    if len(sign_changes) == 0:
        return None
    i = sign_changes[0]
    # Lineare Interpolation zwischen p[i] und p[i+1]
    dp = p_values[i + 1] - p_values[i]
    p_cross = p_values[i] - diff[i] * dp / (diff[i + 1] - diff[i])
    return float(p_cross)


# ======================================================================
# Gemeinsamer Sweep für alle Systemgrößen
# ======================================================================

if __name__ == "__main__":
    rng = np.random.default_rng(42)

    L_values  = [32, 64, 128]
    p_values  = np.arange(0.40, 0.70, 0.02)
    N_SAMPLES = 100

    # Sweep: S(p) und P(p) für jede Systemgröße
    results = {}
    for L in L_values:
        print(f"Aufgabe 5: Sweep für L={L} ({N_SAMPLES} Konf./p-Wert) ...",
              end=" ", flush=True)
        S, P = sweep_S_and_P(L, p_values, N_SAMPLES, rng)
        results[L] = (S, P)
        print("fertig")

    # ======================================================================
    # Aufgabe 5a: p_c aus dem Maximum von S(p)
    # ======================================================================
    fig, ax = plt.subplots(figsize=(9, 6))
    print("\nAufgabe 5a – p_c-Schätzung aus Peak von S(p):")

    for L in L_values:
        S, _ = results[L]
        p_peak = p_values[np.argmax(S)]
        print(f"  L = {L:3d}:  p_c ≈ {p_peak:.4f}")
        ax.plot(p_values, S, "o-", linewidth=1.5, markersize=4, label=f"L = {L}")
        # dünne vertikale Linie am Peak
        ax.axvline(p_peak, linestyle=":", linewidth=0.8, alpha=0.5)

    ax.axvline(P_C_THEORIE, color="black", linestyle="--", linewidth=1.5,
               label=f"$p_c^{{\\rm theor}} = {P_C_THEORIE}$")
    ax.set_xlabel("$p$")
    ax.set_ylabel("$S(p)$")
    ax.set_title("Aufgabe 5a: $p_c$ aus Peak von $S(p)$")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("aufgabe5a_pc_aus_S.png", dpi=150)
    plt.show()
    print("  Gespeichert: aufgabe5a_pc_aus_S.png\n")

    # ======================================================================
    # Aufgabe 5b: p_c aus dem Schnittpunkt der P(p)-Kurven
    # ======================================================================
    fig, ax = plt.subplots(figsize=(9, 6))
    print("Aufgabe 5b – p_c-Schätzung aus Schnittpunkt der P(p)-Kurven:")

    P_arrays = {L: results[L][1] for L in L_values}
    for L in L_values:
        ax.plot(p_values, P_arrays[L], "o-", linewidth=1.5,
                markersize=4, label=f"L = {L}")

    # Schnittpunkte benachbarter Kurvenpaare bestimmen
    crossings = []
    for L_small, L_large in zip(L_values[:-1], L_values[1:]):
        p_cross = find_crossing(p_values, P_arrays[L_small], P_arrays[L_large])
        if p_cross is not None:
            print(f"  Schnittpunkt L={L_small}/L={L_large}:  p_c ≈ {p_cross:.4f}")
            crossings.append(p_cross)
            ax.axvline(p_cross, linestyle=":", linewidth=0.8, alpha=0.5)

    if crossings:
        p_c_mean = np.mean(crossings)
        print(f"  Mittlerer Schätzwert:  p_c ≈ {p_c_mean:.4f}  "
              f"(Theorie: {P_C_THEORIE})")

    ax.axvline(P_C_THEORIE, color="black", linestyle="--", linewidth=1.5,
               label=f"$p_c^{{\\rm theor}} = {P_C_THEORIE}$")
    ax.set_xlabel("$p$")
    ax.set_ylabel("$P(p)$")
    ax.set_title("Aufgabe 5b: $p_c$ aus Schnittpunkt der $P(p)$-Kurven")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("aufgabe5b_pc_aus_P.png", dpi=150)
    plt.show()
    print("  Gespeichert: aufgabe5b_pc_aus_P.png")
