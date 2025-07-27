# Roboter mit Linienverfolgung
## Simulation

- Mithilfe von Pygame werden ein zufälliger Start- und Endpunkt generiert, welche mit einer zufälligen Linie (Catmull-Rom Kurve) verbunden werden.

- Ein Roboter wird mit Ausrichtung auf den Endpunkt am Startpunkt initilisiert

## Steuerungslogik

- Die Steuerung basiert auf drei Sensoren, welche die Linie erkennen
- Mitihlfe eines Reward-Systems und Q-Learning ist der Roboter in der Lage autonom Entscheidungen zu treffen und der Linie zu folgen.
    - Dabei wird der Roboter belohnt, wenn die Sensoren die Linie berühren und wenn er das Ziel erreicht
    - Durch Q-Learning exploriert der Roboter außerdem: d.h. er wählt nicht immer die beste Option, sondern manchmal zufallsbasiert links, geradeaus oder rechts
- Der Roboter funktioniert also mittels Reinforcement Learning 
## 🧰 Vorbereitung: Virtuelle Umgebung aktivieren

Bevor das Projekt gestartet werden kann, muss ein virtuelles Environment erstellt werden:

Einrichten des venv:
python -m venv venv
pip install pygame

Windows (CMD/Powershell):
```cmd
venv\Scripts\activate

macOS / Linux:
source venv/bin/activate

Dann kann der Trainingsprozess ausgeführt werden, dabei reichen 1-2 Durchläufe für eine recht hohe Erfolgschance

Visualisiert wird ein einzelner Durchlauf mittels play.py


