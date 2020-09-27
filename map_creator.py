import pygame

from map import Map
from object_manager import ObjectManager
from tile_manager import TileManager

from gui import Gui

pygame.init()

screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)

clock = pygame.time.Clock()

PATH = "D:/JavaProgs/Mockmon/src/main/resources/"

tm = TileManager(PATH+"/tiles")
om = ObjectManager(PATH+"/objects")

ma = Map(tm, om, PATH+"/world.json")

g = Gui(tm, om, ma)
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
