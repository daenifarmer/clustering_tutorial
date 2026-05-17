# Workshop: Perkolation und Clustereigenschaften

---

## Einführung: Perkolation

* **Perkolation** beschreibt das Entstehen eines zusammenhängenden Pfades durch ein zufälliges Medium
* Modell: 2D-Quadratgitter der Größe L × L
  * Jeder Gitterplatz ist mit Wahrscheinlichkeit p unabhängig **besetzt** (1) oder **leer** (0)
  * Benachbarte besetzte Plätze (oben, unten, links, rechts) bilden einen **Cluster**
* Frage: Ab welchem p existiert ein Cluster, der das Gitter von einer Seite zur anderen durchspannt?

---

## Einführung: Der kritische Punkt

* Für das 2D-Quadratgitter gibt es einen scharfen **Phasenübergang** bei
  * p_c ≈ 0.5927
* Unterhalb von p_c: nur endlich große Cluster, kein durchspannender Cluster
* Oberhalb von p_c: ein "unendlich" großer (durchspannender) Cluster existiert
* Genau bei p_c zeigen alle Observablen **Potenzgesetz-Verhalten** — ein Zeichen für einen Phasenübergang zweiter Ordnung

---

## Übung 1: Hoshen-Kopelman

Dateien: `percolation.py` (Gittergenerierung bereits implementiert, UnionFind über `networkx`)

* Implementieren Sie den **Hoshen-Kopelman-Algorithmus** zur Clusteridentifizierung:
  * Durchlaufen Sie das Gitter zeilenweise von links nach rechts
  * Vergleichen Sie für jeden besetzten Platz die Nachbarn oben und links:
    * Beide unbesetzt → neues Label vergeben
    * Genau ein Nachbar besetzt → dessen Label übernehmen
    * Beide besetzt, gleiches Label → Label übernehmen
    * Beide besetzt, verschiedene Labels → eines übernehmen, Paar als "zu verschmelzen" merken
  * Führen Sie im zweiten Durchgang alle gemerkten Paare zusammen (Union-Find)
* Visualisieren Sie ein beschriftetes Gitter für L = 20 und p = 0.6

**Bonusaufgabe:** Implementieren Sie die Klasse `UnionFind` selbst (mit *path compression* und *union by rank*) und ersetzen Sie damit die `networkx`-Abhängigkeit.

---

## Clustergrößenverteilung: Theorie

* Die **Clustergrößenverteilung** n_s(p) gibt an, wie viele Cluster der Größe s es pro Gitterplatz gibt:
  * n_s(p) = (Anzahl Cluster mit genau s besetzten Plätzen) / L²
* Sie ist eine der zentralen Größen der Perkolationstheorie
* Genau am kritischen Punkt p_c folgt n_s einem Potenzgesetz:

  n_s(p_c) ∝ s^(−τ)

  mit dem universellen Exponenten τ = 187/91 ≈ 2.055 für das 2D-Quadratgitter

* "Universell" bedeutet: der Exponent hängt nicht von den Details des Gitters ab, sondern nur von der Dimension

---

## Übung 2: Clustergrößenverteilung

* Berechnen Sie n_s(p) für p = p_c ≈ 0.5927 auf einem Gitter der Größe L = 200
  * Mitteln Sie über mindestens 200 unabhängige Konfigurationen
  * **Hinweis:** Schließen Sie einen perkolierenden Cluster (falls vorhanden) von der Zählung aus
* Stellen Sie n_s in einem **doppelt-logarithmischen Diagramm** dar
* Das Potenzgesetz n_s ∝ s^(−τ) erscheint im Log-Log-Plot als Gerade — ergänzen Sie diese Referenzlinie mit τ = 187/91
* Können Sie den theoretischen Exponenten bestätigen?

---

## Übung 2: Systemgrößeneinfluss

* Wiederholen Sie die Messung für L = 50, 100, 200 in einem gemeinsamen Plot
* Ab welcher Clustergröße s weicht n_s für kleinere Gitter von der Potenzgesetz-Geraden ab?
* **Diskussion:** Warum gibt es diese Abweichung, und wie hängt sie mit der Systemgröße L zusammen?

---

## Übung 3: Mittlere Clustergröße

* Die **mittlere Clustergröße** S(p) ist definiert als das mit der Clustergröße gewichtete Mittel:

  S(p) = (Σ_s s² · n_s(p)) / (Σ_s s · n_s(p))

  wobei die Summe nur über **nicht-perkolierende** Cluster läuft
* S(p) divergiert am kritischen Punkt: je näher p an p_c, desto größer werden die typischen Cluster
* Plotten Sie S(p) als Funktion von p für verschiedene Gittergrößen L = 32, 64, 128, 256
  * Verwenden Sie p-Werte im Bereich [0.3, 0.75] in Schritten von 0.02
  * Mitteln Sie pro p-Wert über mindestens 200 Konfigurationen

---

## Übung 4: Dichte des perkolierenden Clusters

* Die **Dichte des perkolierenden Clusters** P(p) ist die Wahrscheinlichkeit, dass ein zufällig gewählter besetzter Gitterplatz zum durchspannenden Cluster gehört:

  P(p) = (Größe des perkolierenden Clusters) / (Anzahl besetzter Plätze)

  Falls kein perkolierender Cluster existiert, gilt P(p) = 0
* P(p) ist ein **Ordnungsparameter** des Phasenübergangs:
  * Für p < p_c: P = 0
  * Für p > p_c: P > 0 und wächst mit p
* Plotten Sie P(p) für die gleichen Gittergrößen L = 32, 64, 128, 256 und p-Werte wie in Übung 3

---

## Übung 5: Bestimmung des kritischen Punkts (Bonus)

* Der kritische Punkt p_c lässt sich aus den Plots aus Übung 3 und 4 ablesen:
  * **Aus S(p):** S(p) hat sein Maximum (und divergiert für L → ∞) bei p_c — der Peak verschiebt sich mit wachsendem L gegen p_c
  * **Aus P(p):** Die Kurven für verschiedene L schneiden sich ungefähr bei p_c, da P(p_c, L) näherungsweise L-unabhängig ist
* Bestimmen Sie p_c aus beiden Plots und vergleichen Sie mit dem theoretischen Wert p_c ≈ 0.5927
* **Diskussion:** Welche Methode liefert eine genauere Schätzung, und warum?

---

## Hinweise zu NumPy und Python

* `np.unique(labels, return_counts=True)` gibt Labels und ihre Häufigkeiten zurück
* `np.bincount(arr)` zählt das Vorkommen jedes nicht-negativen ganzzahligen Wertes
* Dictionary Comprehension: `{label: count for label, count in zip(labels, counts)}`
* `np.mean(list_of_arrays, axis=0)` mittelt elementweise über eine Liste von Arrays
* Für den Log-Log-Plot: `plt.xscale('log')` und `plt.yscale('log')`
* Referenzgerade im Log-Log-Plot: `plt.plot(s, C * s**(-tau), '--', label=f'~s^(-{tau:.3f})')`
