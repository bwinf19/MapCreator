import os

import pygame


class ObjectManager:
    def __init__(self, folder):
        self.folder = folder
        self.objects = None
        self.refresh()
        self.selected_object = None

    def refresh(self):
        self.objects = []
        for filename in os.listdir(self.folder):
            self.objects.append(Object(self.folder, filename))

    def get_index(self, name):
        for i in range(len(self.objects)):
            if name == self.objects[i].name:
                return i
        return -1


class Object:
    def __init__(self, folder, filename):
        self.name = filename
        self.path = os.path.join(folder, filename)
        self.image_path = os.path.join(self.path, "image.png")
        self.image = None
        self.image_down = None
        self.image_hover = None
        self.load_image()

    def load_image(self):
        self.image = pygame.image.load(self.image_path)
        self.image_down = self.image.copy()
        pygame.draw.rect(self.image_down, (255, 0, 0), (0, 0, self.image.get_width() - 1, self.image.get_height() - 1),
                         1)
        self.image_hover = self.image.copy()
        pygame.draw.rect(self.image_hover, (255, 150, 150),
                         (0, 0, self.image.get_width() - 1, self.image.get_height() - 1), 1)