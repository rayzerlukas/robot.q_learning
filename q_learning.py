import random  
import math
import time 
import pygame as pg
from roboter import Roboter
import json
from multiprocessing import Manager

# Hyperparameter für Q-Learning
learning_rate = 0.2
discount_factor = 0.8
exploration_rate = 0.6
min_exploration_rate = 0.1
exploration_decay = 0.995
actions = ["links", "geradeaus", "rechts"]

# Q-Tabelle initialisieren
Q = {}

def ist_blau(sensor):
    r, g, b = sensor[:3]
    return r == 0 and g == 0 and b == 255

def get_state(fl, fr, fm):
    return (int(ist_blau(fl)), 
            int(ist_blau(fr)), 
            int(ist_blau(fm))
    )

def choose_action(state, Q_table):
    if state not in Q_table:
        Q_table[state] = {a: 0.0 for a in actions}
    if random.random() < exploration_rate:
        return random.choice(actions)
    return max(Q_table[state].items(), key=lambda x: x[1])[0]

def update_q(state, action, reward, next_state, Q_table):
    if next_state not in Q_table:
        Q_table[next_state] = {a: 0.0 for a in actions}
    next_max = max(Q_table[next_state].values())
    Q_table[state][action] += learning_rate * (reward + discount_factor 
    * next_max - Q_table[state][action])

def run_episode(id, Q_table):
    pg.init()
    Q_local = {}
    hintergrund = pg.Surface((1200, 800))
    hintergrund.fill((255, 255, 255))

    # Start und Endpunkt generieren, 120px Randentfernung
    abstand = 0
    while abstand < 300:
        start = (random.randint(120, 1080), random.randint(120, 680))
        end = (random.randint(120, 1080), random.randint(120, 680))
        dx = start[0] - end[0]
        dy = start[1] - end[1]
        abstand = math.hypot(dx, dy)

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

    # Roboter-Winkel zum Ziel, initialisieren
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    roboter = Roboter(*start, math.degrees(math.atan2(dy, dx)))


    start_time = time.time()

    running = True

    episode_explorade_rate = exploration_rate

    while time.time() - start_time < 60 and running == True:
        # Sensoren lesen
        fl, fm, fr = roboter.sensor_lese(hintergrund)
        state = get_state(fl, fr, fm)

        if state not in Q_local:
                Q_local[state] = {a: 0.0 for a in actions}

        # Aktion wählen mit aktueller exploration_rate 
        if random.random() < episode_explorade_rate:
            action = random.choice(actions)
        else:
            action = max(Q_local[state].items(), key=lambda x: x[1])[0]

        roboter.bewege(action)

        next_state = get_state(*roboter.sensor_lese(hintergrund))
        reward = 5.0 if ist_blau(fm) else 0.5 if ist_blau(fl) or ist_blau(fr) else -1.0

        # Q-Wert aktualisieren
        update_q(state, action, reward, next_state, Q_local)

        # Ziel erreicht
        dist = math.hypot(roboter.x - end[0], roboter.y - end[1])
        if dist < 20:
            reward += 100
            running = False

    # Exploration Rate anpassen
    episode_explorade_rate = max(min_exploration_rate, episode_explorade_rate * exploration_decay)

    for state in Q_local:
        if state not in Q_table:
            Q_table[state] = Q_local[state]
        else:
            for action in actions:
                Q_table[state][action] = max(Q_table[state].get(action, 0), Q_local[state][action])
    pg.quit()
    print(f"Prozess {id} abgeschlossen.")

def run_play_episode():
    pg.init()
    screen = pg.display.set_mode((1200, 800))
    hintergrund = pg.Surface((1200, 800))
    hintergrund.fill((255, 255, 255))

    # Start und Endpunkt generieren, 120px Randentfernung
    abstand = 0
    while abstand < 300:
        start = (random.randint(120, 1080), random.randint(120, 680))
        end = (random.randint(120, 1080), random.randint(120, 680))
        dx = start[0] - end[0]
        dy = start[1] - end[1]
        abstand = math.hypot(dx, dy)

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
    punkte2 = punkte2[:len(punkte2) - 55] + [end]

    # Linie auf Hintergrund zeichnen
    for i in range(len(punkte2) - 1):
        pg.draw.line(hintergrund, (0, 0, 255), punkte2[i], punkte2[i + 1], 4)

    # Roboter-Winkel zum Ziel, initialisieren
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    rad = math.atan2(dy, dx)
    winkel = math.degrees(rad)
    roboter = Roboter(*start, winkel)

    start_time = time.time()
    clock = pg.time.Clock()

    running = True

    while time.time() - start_time < 60 and running == True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        # Sensoren lesen
        fl, fm, fr = roboter.sensor_lese(hintergrund)
        state = get_state(fl, fr, fm)

        # Aktion wählen
        if state not in Q:
            Q[state] = {a: 0.0 for a in actions}
        action = max(Q[state].items(), key=lambda x: x[1])[0]

        roboter.bewege(action)

        screen.fill((255, 255, 255))
        screen.blit(hintergrund, (0, 0))
        roboter.zeichne(screen)
        pg.display.flip()
        clock.tick(60)

        # Endszenarios prüfen: Ziel oder Zeitlimit erreicht
        if time.time() - start_time > 60:  # 60 Sekunden Zeitlimit
            running = False

        dist = math.hypot(roboter.x - end[0], roboter.y - end[1])
        if dist < 20:
            running = False
    pg.quit()     

