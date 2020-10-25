import pygame
import os

pygame.init()

from gui import Gui
from map_manager import MapManager
from object_manager import ObjectManager
from tile_manager import TileManager

loaded = False
while not loaded:
    try:
        with open('config.txt', 'r') as file:
            PATH = file.readlines()[0].split("PATH=")[1]
        for dependency in ['tiles', 'objects']:
            if not os.path.exists(os.path.join(PATH, dependency)):
                raise FileNotFoundError
        loaded = True
    except:
        PATH = input('Please insert a correct Path to the games resource directory:')
        with open('config.txt', 'w') as file:
            file.write('PATH='+PATH)

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
