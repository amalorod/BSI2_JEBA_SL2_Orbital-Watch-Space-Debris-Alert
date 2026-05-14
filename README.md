# Orbital Watch – Space Debris Alert

Ein modulares Python-Programm zur Umwandlung von Weltraumschrott-Koordinaten, Berechnung von ECEF-Koordinaten und Erkennung von Kollisionsrisiken zwischen Satelliten und Debris-Objekten.

---

## 🚀 Funktionen & Challenges

*   **Challenge 1:** Wandelt GPS-Koordinaten im Grad-Minuten-Sekunden-Format (GMS) in Dezimalgrad um. Breiten- und Längengrade werden anschließend summiert und miteinander multipliziert.
*   **Challenge 2:** Nutzt die Dezimalkoordinaten aus Challenge 1 und konvertiert diese mithilfe von WGS-84-Konstanten in ECEF-Koordinaten (Fehlerminimierung durch Verzicht auf frühzeitige Rundung).
*   **Challenge 3:** Lädt Satellitendaten, rechnet diese von Metern in Kilometer um und ermittelt über die euklidische Distanz alle Debris-Objekte innerhalb eines 1-km-Radius zu einem Satelliten.

---

## 🛠️ Technologie-Stack

*   **Programmiersprache:** Python (ideal für CSV-Verarbeitung, mathematische Berechnungen und Prototyping)
*   **Benutzeroberflächen:** CLI (Befehlszeile) und GUI (Grafische Oberfläche)
*   **Testing:** Pytest zur Validierung von Soll-Ist-Werten

---

## 💻 Installation & Ausführung

### Voraussetzungen
Stelle sicher, dass du dich im richtigen Projektverzeichnis befindest. Falls du im Überordner startest, wechsle zuerst in das Projektverzeichnis:
```bash
cd orbital-watch
```

### Einzelne Challenges starten
Die Challenges können separat über das Terminal aufgerufen werden:
```bash
python -m src.challenge1
python -m src.challenge2
python -m src.challenge3
```

### Hauptprogramm ausführen
Um alle Challenges nacheinander automatisiert auszuführen:
```bash
python -m src.main
```

### GUI und Tests starten
Für die grafische Oberfläche oder die Validierung der Testergebnisse nutzt du folgende Befehle:
```bash
python -m src.gui
pytest
```

---

## 📂 Projektstruktur & Architektur

Das Programm ist strikt modular aufgebaut:
*   **Modulare Aufteilung:** Gemeinsame Hilfsfunktionen liegen in separaten Dateien.
*   **Einzelaufrufe:** Jede Challenge sowie die GUI existieren als eigenständige Module.

---

## 🤖 KI-Nutzung & Learnings

Das Projekt diente dem Einstieg in die Programmiersprache Python unter intensiver Nutzung von KI-Tools (**GitHub Copilot** und **VSCode-interne KI**):
*   **Architektur:** Die KI half bei der Definition der Ordnerstruktur, Modulaufteilung und Fehlervermeidung.
*   **Kollaboration:** Es wurden keine fertigen Lösungen kopiert, sondern Vorschläge im Dialog an die eigenen Anforderungen angepasst.

---

## 🔧 Fehlerbehebung & Validierung (Lessons Learned)

Während der Entwicklung wurden folgende Kernprobleme analysiert und behoben:
*   **Importfehler:** Korrektur von Modulnamen und Ergänzung fehlender `__init__.py`-Dateien.
*   **Daten-Mapping:** Behebung von Abweichungen bei CSV-Spaltennamen (z. B. `Long`, `Alt_km`, `X_m`, `Y_m`, `Z_m`).
*   **Präzision:** Frühes Runden auf zwei Nachkommastellen führte zu Abweichungen. Durch die Umstellung auf späte Rundung erzielt Challenge 2 Ergebnisse, die nahezu identisch mit dem Referenzwert (`-359.776.16973`) sind.
