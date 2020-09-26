import os

import pygame


class TileManager:
    def __init__(self, folder):
        self.tiles = []
        for filename in os.listdir(folder):
            if filename.endswith(".png"):
                self.tiles.append(Tile(folder, filename))
        self.selected_tile = None

    def get_index(self, name):
        for i in range(len(self.tiles)):
            if name == self.tiles[i].name:
                return i
        return None


class Tile:
    def __init__(self, folder, filename):
        self.name = ".".join(filename.split(".")[:-1])
        self.image = pygame.image.load(os.path.join(folder, filename))
        self.image_down = self.image.copy()
        pygame.draw.rect(self.image_down, (255, 0, 0), (0, 0, self.image.get_width()-1, self.image.get_height()-1), 1)
        self.image_hover = self.image.copy()
        pygame.draw.rect(self.image_hover, (255, 150, 150), (0, 0, self.image.get_width()-1, self.image.get_height()-1), 1)
