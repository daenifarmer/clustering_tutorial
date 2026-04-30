# Workshop: Perkolation und Clustereigenschaften

---

Einführung in Perkolation

---

## Übung 1: Hoshen-Kopelmann

Dateien: (Vorschlag: Struktur wie in PAC (Generierung fertig), UnionFind ist implementiert mit der Bibliothek)

* Implementieren Sie den Hoshen-Kopelmann Algorithmus zur Clusteridentifizierung.
* Bonuspunkt: Ergänzen Sie das Projekt um die Klasse UnionFind und verzichten Sie auf die Verwendung von Networkx

---

hier Beschreibung des kritischen Punkts und Wert für 2D-Quadratgitter, Formel für n(S) angeben(?) und erklären, was es mir sagt


## Übung 2: Clustergrößenverteilung

* Plotten Sie die Clustergrößenverteilung n(S) am kritischen Punkt auf einem Gitter der Größe L = 200 in log-log Darstellung. Mitteln Sie dabei über verschiedene Besetzungskonfigurationen.
* Am kritischen Punkt folgt n(S) der Beziehung
    n(S) prop. S^(-tau)
Im 2D Gitter ist tau gegeben durch tau = 187/91
* Ergänzen Sie Ihren Plot um diese Funktion. Können Sie den exponentiellen Verlauf/den kritischen Exponenten bestätigen?

Tipp: perkolierendes Cluster ausschließen
---

## Übung 3: mittlere Clustergröße

* Plotten Sie die mittlere Clustergröße in Abhängigkeit von p für verschiedene Gittergrößen L.
* S(p) = ... angeben.



---

## Übung 4: Dichte des perkolierenden Clusters

heißt: Wahrscheinlichkeit dafür, dass eine zufällig ausgewählte Gitterstelle besetzt ist und zum perkolierenden Cluster gehört. 

* Plotten Sie die Dichte P(p) in Abhängigkeit der Besetzungswahrscheinlichkeit für verschiedene Gittergrößen.

---

## Übung 5: Bestimmung des kritischen Punkts (ggf. Bonus)

* Bestimmen Sie aus den Plots aus Teilaufgabe 3 und 4 den Wert für den kritischen Punkt p_c und vergleichen Sie ihn mit dem theoretischen.