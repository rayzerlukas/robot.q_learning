import pygame as pg
from roboter import Roboter

pg.init()

pg.display.set_caption("RaspberryBot Simulation")
screen = pg.display.set_mode((800, 600))    

hintergrund = pg.Surface((800, 600))
hintergrund.fill((255, 255, 255))

clock = pg.time.Clock()
running= True

roboter = Roboter(400, 300)

def ist_blau(sensor):
    r,g,b = sensor[:3]
    return r == 0 and g == 0 and b == 255

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

    #Winkellogik
    fl, fr, fm = roboter.sensor_lese(hintergrund)
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
pg.quit()
exit()