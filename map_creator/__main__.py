import pygame
import os

os.environ['SDL_AUDIODRIVER'] = 'dsp'

pygame.init()

from mapgui import MapGui
from npcgui import NpcGui
from map_manager import MapManager
from object_manager import ObjectManager
from tile_manager import TileManager
from npc_manager import NpcManager
from npc_editor import NpcEditor

loaded = False
while not loaded:
    try:
        PATH = open('config.txt', 'r').readlines()[0].split("PATH=")[1]
        for dependency in ['tiles', 'objects']:
            if not os.path.exists(os.path.join(PATH, dependency)):
                raise FileNotFoundError
        loaded = True
    except:
        PATH = input('Please insert a correct Path to the games resource directory:')
        open('config.txt', 'w').write('PATH=' + PATH)


class GuiManager:
    def __init__(self, path):
        self.screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)

        self.clock = pygame.time.Clock()

        tm = TileManager(os.path.join(path, "tiles"))
        om = ObjectManager(os.path.join(path, "objects"))
        trm = NpcManager(os.path.join(path, "skins"))

        mm = MapManager(PATH, os.path.join(path, "objects"), tm, om, trm, self)
        self.mg = MapGui(tm, om, trm, mm)
        self.mg.rebuild_scene(self.screen.get_width(), self.screen.get_height())
        self.npce = NpcEditor()
        self.ng = NpcGui(self.npce, trm, self)
        self.ng.rebuild_scene(self.screen.get_width(), self.screen.get_height())

        self.currg = self.mg

    def load_npc(self, pos, npc):
        self.npce.set_npc(pos, npc)
        self.ng.entry()
        self.ng.rebuild_scene(self.screen.get_width(), self.screen.get_height())
        self.currg = self.ng

    def save_npc_and_load(self, pos, npc):
        self.mg.map_manager.current_map.change_npc(pos, npc)
        self.mg.map_manager.save()
        self.mg.rebuild_scene(self.screen.get_width(), self.screen.get_height())
        self.currg = self.mg

    def start(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                self.currg.handle_event(event)

            self.screen.fill((0, 0, 0))

            self.currg.render(self.screen)

            pygame.display.flip()

            self.clock.tick()


g = GuiManager(PATH)
g.start()
