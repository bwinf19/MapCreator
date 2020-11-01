import os

import pygame


class NpcManager:
    def __init__(self, folder):
        self.npcs = []
        for filename in os.listdir(folder):
            self.npcs.append(Npc(folder, filename))
        self.selected_npc = None

    def get_index(self, name):
        for i in range(len(self.npcs)):
            if name == self.npcs[i].name:
                return i
        return -1


class Npc:
    def __init__(self, folder, filename):
        self.name = filename
        self.image = pygame.image.load(os.path.join(folder, filename, "front.png"))
        self.image_down = self.image.copy()
        pygame.draw.rect(self.image_down, (255, 0, 0), (0, 0, self.image.get_width() - 1, self.image.get_height() - 1),
                         1)
        self.image_hover = self.image.copy()
        pygame.draw.rect(self.image_hover, (255, 150, 150),
                         (0, 0, self.image.get_width() - 1, self.image.get_height() - 1), 1)
