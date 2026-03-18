# Monopoly CLI-Version in Python 
== Entwickler: 
- Daniel Lohrengel
- Vivian Heidt
- ~~Tobias Kipping~~

---

## Projektziel: 

Dieses Projekt implementiert eine einfache textbasiertes Version von Monopol, welches über ein Command Line Interface (CLI) gespielt werden kann. 
Das Projekt wurde mittels der Programmiersprache Python entwickelt unter der Verwendung von Standard Bibliotheken.
Die Implementierung konzentriert sich bewusst auf die Kernmechaniken des Spiels.
Komplexe Sonderregeln wurden zugunsten einer klaren Architektur und Verständlichkeit reduziert.

---

## Grundlegendes: 
Die Software aus den offiziellen Spielregeln abgeleitet:
1. Würfeln
2. Bewegung der Spielfigur
3. Ausführen der Feldaktion
4. Übergang zum nächsten Spieler

Für Geldbeträge werden ausschließlich integer verwendet, 
da das Monopoly-Spiel keine float vorsieht und so Rundungsfehler vermieden werden.

---

## Architektur übersicht:
- 📁 Domain: 
   -  enthält fachliche Kernlogik so wie die Regeln des Spiels.
      - `Game` 🎮: enthält Ablaufsteuerung & kompletten Spielzustand.
      - `Player`👤: repräsentiert einen Spieler mit seinem aktuellen Zustand (Position, Geld, Besitz). 
      - `Board` 🗺: enthält keine Logik sondern Sammlung der Felder (Tiles).
      - `Tile ` ⚙️: ist Abstrakte Basisklasse für Felder. Definiert das Verhalten beim Beitritt des Feldes. 
      - `Money` 💵: enthät die Logik des aktuellen Saldos des Spielers (z.B. Addition, Subtraktion, Vergleich). 
      - `Cards` 🗃️: enthält Ereigniskarten, die Einfluss auf den Spielverlauf nehmen.
      - `Position`📍: value Object zur Darstellung der Position eines Spielers auf dem Spielfeld.
  
- 📁 Application:
   - Enthält die Anwendungslogik und übernimmt die komplette Steuerung des Spiels aus Sicht des Spielers (koordinert die Logik der Domainobjekte).
     -  `StartGame`: erstellt das Spiel, erstellt die Spieler, erstellt das Board, setzt Startzustand. 
     -  `PlayTurn`: zentraler UseCase stellt ein Spielerablauf dar wenn ein Spieler am Zug ist (bestimmt Spieler, Würfeln, Spieler bewegt sich, Feld wird ausgeführt).
     -  `BuyProperty`: Grundstückslogik wenn ein Spieler auf ein Feld landet. (Grundstück verfügbar?, prüfen ob genug Geld, Geldtransaktionen durchführen). 
     -  `PayRent`: tritt in Aktion wenn ein Spieler auf das Feld eines anderen Spielers landet (Miete Berechnen, Geld Übertragen, Grundstück erweitern).

- 📁 Infrastuctue:
  - Verbindet das entwickelte Programm mit der Außenweld und kapselt technische Details.
      - `DiceRandomService`: mittels Standardbibliothek Random wird mittels Python ein Würfelergebniss erzeugt.
      - `ConsoleOutput`, `ConsoleInput`: liest-/schreibt benötigten Ein bzw. Ausgaben des Anwenders.
      - `JsonGameRepository`: speichert und lädt Spielstände aus einer Datei (Logging oder Dateizugriffe).

- 📁 Presentation:
  - Enthällt die Benutzerschnittstelle dient als Benutzeroberfläche. 
      - CLI.
      - Menüs.
      - Eingabeauforderungen: “Möchtest du dieses Grundstück kaufen?”
      - Ausgabe von Texten: “Spieler 1 ist am Zug”

---
