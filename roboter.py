import pygame as pg
class Roboter:
    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.winkel = w
        self.geschwindigkeit = .5
        self.drehrate = 3

        self.image = pg.Surface((50, 30), pg.SRCALPHA)
        pg.draw.rect(self.image, (0, 0, 255), (0, 0, 50, 30))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        import math
        rad = math.radians(self.winkel)
        dx = self.geschwindigkeit * math.cos(rad)
        dy = self.geschwindigkeit * math.sin(rad)
        self.x += dx
        self.y += dy
        self.winkel %= 360
        self.image = pg.transform.rotate(self.original_image, -self.winkel)
        self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))

    def zeichne(self, surface):
        import math

        # Sensoren relativ zu rect.center berechnen
        offset = 15
        abstand = 18
        cx, cy = self.rect.center
        rad = math.radians(self.winkel)

        # Sensorpositionen
        lx = int(cx + offset * math.cos(rad) - abstand * math.sin(rad))
        ly = int(cy + offset * math.sin(rad) + abstand * math.cos(rad))
        rx = int(cx + offset * math.cos(rad) + abstand * math.sin(rad))
        ry = int(cy + offset * math.sin(rad) - abstand * math.cos(rad))
        mx = int(cx + 1.5 * offset * math.cos(rad))
        my = int(cy + 1.5 * offset * math.sin(rad))

        # Zeichnen Roboterbild
        surface.blit(self.image, self.rect)

        # Linie Richtung vor Roboter (Fahrtrichtung)
        end_x = cx + 20 * math.cos(rad)
        end_y = cy + 20 * math.sin(rad)
        pg.draw.line(surface, (0, 0, 0), (cx, cy), (round(end_x), round(end_y)), 2)

        # Sensoren visualisieren
        pg.draw.circle(surface, (255, 0, 0), (lx, ly), 5)
        pg.draw.circle(surface, (255, 0, 0), (rx, ry), 5)
        pg.draw.circle(surface, (255, 255, 0), (mx, my), 5)


    def sensor_lese(self, surface):
        import math
        rad = math.radians(self.winkel)
        offset = 15
        abstand = 18  # Abstand links/rechts vom Zentrum
        cx, cy = self.rect.center
        
        # Mittlere Sensor
        mx = int(cx + offset * math.cos(rad))
        my = int(cy + offset * math.sin(rad))

        # Linker Sensor
        lx = int(cx + offset * math.cos(rad) - abstand * math.sin(rad))
        ly = int(cy + offset * math.sin(rad) + abstand * math.cos(rad))

        # Rechter Sensor
        rx = int(cx + offset * math.cos(rad) + abstand * math.sin(rad))
        ry = int(cy + offset * math.sin(rad) - abstand * math.cos(rad))

        try:
            farbe_mitte = surface.get_at((mx, my))
            farbe_links = surface.get_at((lx, ly))
            farbe_rechts = surface.get_at((rx, ry))
        except IndexError:
            farbe_links = farbe_rechts = farbe_mitte = (255, 255, 255, 255)

        return farbe_links, farbe_rechts, farbe_mitte   
    
    # für q_learning.py
    def bewege(self, aktion):
        if aktion == "links":
            self.winkel += self.drehrate
        elif aktion == "rechts":
            self.winkel -= self.drehrate
        elif aktion == "geradeaus":
            pass
        self.update()
