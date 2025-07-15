# 🤖 RaspberryPi Roboter mit Linienverfolgung

## 🚧 Projektphasen

- **Phase 1** – Simulation mit einfacher Logik *(aktueller Stand)*
- **Phase 2** – Einfache Logik auf Roboter mit Raspberry Pi anwenden
- **Phase 3** – KI verwenden, um durch Lernen Fehlerbewältigung zu ermöglichen
- **Phase 4** – KI auf Roboter anwenden

## 🧪 Aktueller Stand: Phase 1 – Simulation

In Python mit `pygame` wurde eine 2D-Simulation erstellt:

- Ein rechteckiger Roboter fährt automatisch über eine frei mit der Maus gezeichnete blaue Linie.
- Drei Sensoren vorne am Roboter erkennen, ob sie sich über einer Linie befinden (links, mitte, rechts).
- Die Fahrtrichtung (Winkel) wird durch einfache Entscheidungslogik korrigiert, um mittig auf der Linie zu bleiben.
- Linien können live per Maus gezeichnet und mit der Taste `C` gelöscht werden.

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
```cmd
venv\Scripts\activate

macOS / Linux:
source venv/bin/activate

dann "python main.py"

und mit gedrückter linker Maustaste eine Linie zeichnen - Roboter folgt.
