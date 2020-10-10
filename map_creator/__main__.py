import json
import pygame
import os

pygame.init()

from gui import Gui
from map_manager import MapManager
from object_manager import ObjectManager
from tile_manager import TileManager

with open('config.json') as json_file:
    PATH = json.load(json_file)['PATH']

screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)

clock = pygame.time.Clock()

tm = TileManager(os.path.join(PATH, "tiles"))
om = ObjectManager(os.path.join(PATH, "objects"))

mm = MapManager(PATH, os.path.join(PATH, "objects"), tm, om)

g = Gui(tm, om, mm)
g.rebuild_scene(640, 480)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        g.handle_event(event)

    screen.fill((0, 0, 0))

    g.render(screen)

    pygame.display.flip()

    clock.tick()
