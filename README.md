# Roboter mit Linienverfolgung

## Projektphasen

- **Phase 1** – Simulation mit einfacher Logik *(aktueller Stand)*
- **Phase 2** – KI verwenden, um durch Lernen Fehlerbewältigung zu ermöglichen

## 🧪 Aktueller Stand: Phase 1 – Simulation

- Start- und Endpunkt werden zufallsbasiert erstellt und diskret verbunden
- Roboter folgt mit einfacher Logik Linie zum Ziel
- Logging System
      - Datenerfassung (Ziel erreicht, Dauer, Sensoreneffizienz)
      - Möglichkeit mehrere Durchläufe auf einmal zu starten

## 🧠 Steuerungslogik

- Wenn der mittlere Sensor blau sieht: nur feine Korrekturen mit äußeren Sensoren.
- Wenn der mittlere Sensor leer ist, aber äußere aktiv sind: stärkere Korrektur in Richtung der Linie.
- Wenn kein Sensor blau sieht: leichte Drehung zur rechten Seite (kann später durch "Suchmodus" verbessert werden).

## 🧰 Vorbereitung: Virtuelle Umgebung aktivieren

Bevor du das Projekt startest, aktiviere deine virtuelle Umgebung:

Einrichten des venv:
python -m venv venv
pip install pygame

Windows (CMD/Powershell):
cmd
venv\Scripts\activate

macOS / Linux:
source venv/bin/activate

dann "python main.py"

und mit gedrückter linker Maustaste eine Linie zeichnen - Roboter folgt.
