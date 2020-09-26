import pygame

from object_manager import ObjectManager
from tile_manager import TileManager

from gui import Gui

pygame.init()

screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)

clock = pygame.time.Clock()

tm = TileManager("tiles")
om = ObjectManager("objects")

g = Gui(tm, om)
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
