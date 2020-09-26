import os

import pygame


class ObjectManager:
    def __init__(self, folder):
        self.objects = []
        for filename in os.listdir(folder):
            self.objects.append(Object(folder, filename))
        self.selected_object = None

    def get_index(self, name):
        for i in range(len(self.objects)):
            if name == self.objects[i].name:
                return i
        return None


class Object:
    def __init__(self, folder, filename):
        self.name = filename
        self.image = pygame.image.load(os.path.join(folder, filename, "image.png"))
        self.image_down = self.image.copy()
        pygame.draw.rect(self.image_down, (255, 0, 0), (0, 0, self.image.get_width()-1, self.image.get_height()-1), 1)
        self.image_hover = self.image.copy()
        pygame.draw.rect(self.image_hover, (255, 150, 150), (0, 0, self.image.get_width()-1, self.image.get_height()-1), 1)
