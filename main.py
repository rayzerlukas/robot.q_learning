import pygame as pg
from roboter import Roboter
import random
import math
import time
import json

#settings
pg.init()
pg.display.set_caption("RaspberryBot Simulation")
screen = pg.display.set_mode((1200, 800))    
hintergrund = pg.Surface((1200, 800))
hintergrund.fill((255, 255, 255))

# Zufälligen Start- und Endpunkt generieren, mit Mindestabstand von 300 Pixeln
abstand = 0
while abstand < 300:
    start = (random.randint(0, 1200), random.randint(0, 800))
    end = (random.randint(0, 1200), random.randint(0, 800))
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    abstand = math.hypot(dx, dy)

pg.draw.circle(hintergrund, (255, 0, 255), end, 10)

# Zwischenpunkte zwischen Start und Endpunkt generieren
punkte = [start]
anzahl_punkte = 4
for i in range(1, anzahl_punkte + 1):
    x = start[0] + (end[0] - start[0]) * i / anzahl_punkte + random.randint(-120, 120)
    y = start[1] + (end[1] - start[1]) * i / anzahl_punkte + random.randint(-120, 120)
    punkte.append((x, y))
punkte.append(end)
punkte = [start] + punkte + [end] # dupliziert für Catmull-Rom Kurve

# Catmull-Rom Kurve zeichnen
punkte2 = []
for i in range(len(punkte) - 3):
    p0, p1, p2, p3 = punkte[i:i + 4]
    for t in range(0, 101):  # 101 Schritte für eine glatte Kurve
        t /= 100.0
        x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t**2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t**3)
        y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t**2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t**3)
        punkte2.append((x, y))

# Glätten des Endes
punkte2 = punkte2[:len(punkte2) - 70]
punkte2.append(end)

#Zeichnen der Kurve
for i in range(len(punkte2) - 1):
    pg.draw.line(hintergrund, (0, 0, 255), punkte2[i], punkte2[i + 1], 4)

clock = pg.time.Clock()
running= True

# Winkelausrichtung des Roboters auf den Endpunkt
dx = end[0] - start[0]
dy = end[1] - start[1]
rad = math.atan2(dy, dx)
winkel = math.degrees(rad)
roboter = Roboter(*start, winkel)

def ist_blau(sensor):
    r,g,b = sensor[:3]
    return r == 0 and g == 0 and b == 255

start_time = time.time()

ergebnis = 0
sensordauer = 0

# Hauptschleife
last_pos = None
while running:
    screen.blit(hintergrund, (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        mdown = pg.mouse.get_pressed()
        current_pos = pg.mouse.get_pos()
        if mdown[0]:
            if last_pos is not None:
                pg.draw.line(hintergrund, (0, 0, 255), last_pos, current_pos, 5)
            last_pos = current_pos
        else:
            last_pos = None

        if event.type == pg.KEYDOWN and event.key == pg.K_c:
            hintergrund.fill((255, 255, 255))
    
    # Sensoren lesen
    fl, fr, fm = roboter.sensor_lese(hintergrund)    

    # Punktesystem
    # Punkte sammeln, wenn Roboter auf der Linie ist und wenn Ziel erreicht ist
    dt = clock.tick(144) / 1000.0  # Zeit in Sekunden seit letztem Frame
    if ist_blau(fm):
        sensordauer += dt
    elif ist_blau(fl) or ist_blau(fr):
        sensordauer += dt * 0.5

    if time.time() - start_time > 60:  # 60 Sekunden Zeitlimit
        print("Zeitlimit erreicht! Simulation wird beendet.")
        ergebnis = -1
        running = False

    dist = math.hypot(roboter.x - end[0], roboter.y - end[1])
    if dist < 10:
        print("Ziel erreicht!")
        ergebnis = 1
        running = False

    #Winkellogik
    if ist_blau(fm):
        # Mittlerer Sensor auf der Linie
        if ist_blau(fl) and not ist_blau(fr):
            roboter.winkel += .15 * roboter.drehrate  
        elif ist_blau(fr) and not ist_blau(fl):
            roboter.winkel -= .15 * roboter.drehrate  
        else:
            pass
    else:
        # Mittlerer Sensor nicht auf Linie
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

    clock.tick(144)
    pg.display.flip()

# Logging
log = {
    "ergebnis": ergebnis,
    "zeit": time.time() - start_time,
    "sensordauer": sensordauer
}

with open("simulation_log.json", "a") as f:
    json.dump(log, f)
    f.write("\n")

pg.quit()
exit()