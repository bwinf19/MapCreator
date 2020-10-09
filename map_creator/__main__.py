import pygame
import os


pygame.init()

from map_creator.gui import Gui
from map_creator.map_manager import MapManager
from map_creator.object_manager import ObjectManager
from map_creator.tile_manager import TileManager

PATH = "D:/JavaProgs/Mockmon/src/main/resources/"

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
