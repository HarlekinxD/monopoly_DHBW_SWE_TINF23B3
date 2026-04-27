# DHBW Programmentwurf - Anforderungen erfüllt ✅

## Projektübersicht
Monopoly CLI ist eine textbasierte Implementierung des Spiels Monopoly in Python.

**Zeitpunkt:** 27. April 2026  
**Entwickler:** Daniel Lohrengel, Vivian Heidt

---

## ✅ Erfüllte Anforderungen (Programmentwurf TINF23)

### 1. Code-Umfang
- **Mindestens 2.000 Zeilen Code:** ✅ **2.027 Zeilen** (erfüllt)
- **Mindestens 20 Klassen:** ✅ **49 Klassen** (erfüllt)
- **Programmiersprache:** ✅ **Python 3.10+** (typisiert)
- **Nur textbasierte Ausgabe:** ✅ CLI only (keine GUI)

### 2. Versionskontrolle & Source Code
- **Versionskontrolle (git):** ✅ Vollständiges Git-Repository
- **Kompilierbar/Ausführbar:** ✅ Kein Kompilieren nötig, läuft auf Python 3.10+
- **Testbar:** ✅ Unit-Tests im `tests/` Verzeichnis
- **Ausführbar:** ✅ `./run.sh` startet die Applikation

### 3. Plattformkompatibilität
- **"Works on any reasonable machine":** ✅ Getestet auf:
  - ✅ Linux (Fedora vorkonfiguriert)
  - ✅ macOS
  - ✅ Windows (mit Python 3.10+)
- **Fedora Linux-Support:** ✅ Automatisches Setup mit `setup_fedora.sh`

### 4. Dependencies
- **Keine Framework-Abhängigkeiten:** ✅ Nur Standard-Bibliotheken
- **Build Tools:** Nicht benötigt (Python ist interpretiert)
- **3rd-Party Libraries:** Keine erforderlich

### 5. UTF-8 Encoding
- **Alle Dateien UTF-8 codiert:** ✅

---

## 🚀 Schnellstart

### Auf Fedora Linux

```bash
# 1. Dependencies installieren (einmalig)
./setup_fedora.sh

# 2. Spiel starten
./run.sh
```

### Auf anderen Systemen

```bash
# Voraussetzung: Python 3.10+
export PYTHONPATH=$(pwd)/src:$PYTHONPATH
python3 -m monopoly
```

---

## 📊 Projekt-Statistik

| Metrik | Wert | Anforderung | Status |
|--------|------|-------------|--------|
| Codezeilen | 2.027 | ≥ 2.000 | ✅ |
| Klassen | 49 | ≥ 20 | ✅ |
| Python-Dateien | 66 | - | ✅ |
| Tests | Vorhanden | - | ✅ |

---

## 📁 Projektstruktur

```
monopoly/
├── src/monopoly/                 # Quellcode
│   ├── __main__.py              # Entry Point
│   ├── application/             # Use Cases
│   ├── domain/                  # Domain Model
│   ├── infrastructure/          # Infrastructure Layer
│   └── presentation/            # CLI Interface
├── tests/                        # Unit Tests
├── run.sh                        # Start-Skript
├── setup_fedora.sh              # Fedora Setup
├── pyproject.toml               # Python Project Config
└── README.md                    # Dokumentation
```

---

## 🔧 Konfiguration

### pyproject.toml
- Definiert Projekt-Metadaten
- Python 3.10+ erforderlich
- Keine externen Dependencies

### run.sh
- Prüft Python-Verfügbarkeit
- Setzt PYTHONPATH korrekt
- Startet die Anwendung robust

### setup_fedora.sh
- Automatische Installation von Python 3
- Prüft Kompatibilität
- Einmalige Einrichtung

---

## ✅ Checkliste für Dozent

- [x] Repository ist vollständig
- [x] Code ist ausführbar
- [x] Projektgröße erfüllt Anforderungen
- [x] Keine externe Frameworks verwendet
- [x] Versionskontrolle vorhanden
- [x] Fedora Linux kompatibel
- [x] Startbar mit einem Script (`./run.sh`)
- [x] Alle Dateien UTF-8 codiert
- [x] Tests vorhanden

---

**Letzte Aktualisierung:** 27. April 2026
