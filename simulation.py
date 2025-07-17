import pygame as pg
from roboter import Roboter
import random
import math
import time
import json
from multiprocessing import Process

def simulation_run(id):
    pg.init()
    # Kein Fenster: nur Surface im Speicher
    screen = pg.Surface((1200, 800))
    hintergrund = pg.Surface((1200, 800))
    hintergrund.fill((255, 255, 255))

    # Zufälligen Start- und Endpunkt generieren, Mindestabstand 300px
    abstand = 0
    while abstand < 300:
        start = (random.randint(120, 1080), random.randint(120, 680))  # min 120px Rand
        end = (random.randint(120, 1080), random.randint(120, 680))
        dx = start[0] - end[0]
        dy = start[1] - end[1]
        abstand = math.hypot(dx, dy)

    # Zielpunkt markieren
    pg.draw.circle(hintergrund, (255, 0, 255), end, 10)

    # Zwischenpunkte generieren
    punkte = [start]
    anzahl_punkte = 4
    for i in range(1, anzahl_punkte + 1):
        x = start[0] + (end[0] - start[0]) * i / anzahl_punkte + random.randint(-120, 120)
        y = start[1] + (end[1] - start[1]) * i / anzahl_punkte + random.randint(-120, 120)
        punkte.append((x, y))
    punkte.append(end)
    punkte = [start] + punkte + [end]  # Dupliziert für Catmull-Rom

    # Catmull-Rom Kurve
    punkte2 = []
    for i in range(len(punkte) - 3):
        p0, p1, p2, p3 = punkte[i:i + 4]
        for t in range(0, 101):
            t /= 100.0
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t**2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t**3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t**2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t**3)
            punkte2.append((x, y))
    punkte2 = punkte2[:len(punkte2) - 70] + [end]

    # Linie auf Hintergrund zeichnen
    for i in range(len(punkte2) - 1):
        pg.draw.line(hintergrund, (0, 0, 255), punkte2[i], punkte2[i + 1], 4)

    # Roboter-Winkel zum Ziel
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    rad = math.atan2(dy, dx)
    winkel = math.degrees(rad)
    roboter = Roboter(*start, winkel)

    def ist_blau(sensor):
        r, g, b = sensor[:3]
        return r == 0 and g == 0 and b == 255

    clock = pg.time.Clock()
    running = True
    start_time = time.time()
    ergebnis = 0
    sensordauer = 0

    while running:
        # Sensoren lesen
        fl, fr, fm = roboter.sensor_lese(hintergrund)

        dt = clock.tick(144) / 1000.0
        if ist_blau(fm):
            sensordauer += dt
        elif ist_blau(fl) or ist_blau(fr):
            sensordauer += dt * 0.5

        if time.time() - start_time > 60:
            ergebnis = -1
            running = False

        dist = math.hypot(roboter.x - end[0], roboter.y - end[1])
        if dist < 10:
            ergebnis = 1
            running = False

        if ist_blau(fm):
            if ist_blau(fl) and not ist_blau(fr):
                roboter.winkel += .15 * roboter.drehrate
            elif ist_blau(fr) and not ist_blau(fl):
                roboter.winkel -= .15 * roboter.drehrate
        else:
            if ist_blau(fl) and not ist_blau(fr):
                roboter.winkel += 3 * roboter.drehrate
            elif ist_blau(fr) and not ist_blau(fl):
                roboter.winkel -= 3 * roboter.drehrate
            elif ist_blau(fl) and ist_blau(fr):
                roboter.winkel += 0.5 * roboter.drehrate
            else:
                roboter.winkel += roboter.drehrate * 0.2

        roboter.update()
        roboter.zeichne(screen)

    log = {
        "id": id,
        "ergebnis": ergebnis,
        "zeit": time.time() - start_time,
        "sensordauer": sensordauer
    }

    with open(f"simulation_log.json", "a") as f:
        json.dump(log, f)
        f.write("\n")

    pg.quit()


if __name__ == "__main__":
    prozesse = []
    anzahl_simulationen = 10

    for i in range(anzahl_simulationen):
        p = Process(target=simulation_run, args=(i,))
        p.start()
        prozesse.append(p)

    for p in prozesse:
        p.join()

    print("Alle Simulationen abgeschlossen.")
