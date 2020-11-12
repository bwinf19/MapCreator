import pygame

from gui_tools import Button, GuiContainer, TextField, ObjectGuiContainer

import os
import json


class ObjectGui:
    def __init__(self, gm, om):
        self.last_width = 500
        self.last_height = 500
        self.gm = gm

        self.object_manager = om

        self.object = None
        self.name = 'ERROR! PLS ASK'
        self.data = None

        img = pygame.Surface((100, 100))
        img.fill((150, 150, 150))

        self.bg = ObjectGuiContainer([], (32, 64), extras=[])

        self.back_button = Button(0, 0, 120, 30, text="Back", image_normal=img,
                                  callback=self.gm.load_map)

        self.save_button = Button(0, 40, 120, 30, text="Save", image_normal=img,
                                  callback=lambda: None)

        self.name_text = Button(140, 0, 180, 30, text=self.name)

        self.create_config_button = Button(140, 40, 500, 30, text=self.name, image_normal=img)

        self.rebuild_scene(self.last_width, self.last_height)

    def entry(self):
        pass

    def exit(self):
        pass

    def set_object(self, x):
        self.object = self.object_manager.objects[x]
        self.name = self.object.name
        self.name_text.set_text('Name: ' + self.name, True, fit_rect=True)
        config = os.path.join(self.object.path, 'config.json')

        if os.path.isfile(config):
            line = open(config, "r").readline()
            self.data = json.loads(line)
        else:
            self.data = None
            self.create_config_button.set_text('Create config.json for '+self.name, True)

    def rebuild_scene(self, width, height):
        self.bg.set_rect(0, 0, width, height)

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.rebuild_scene(event.w, event.h)
        self.save_button.handle_event(event)
        self.back_button.handle_event(event)
        self.create_config_button.handle_event(event)

    def render(self, screen):
        self.bg.draw(screen)

        image = self.object.image
        rect = image.get_rect(topleft=(120, 100))
        screen.blit(image, rect)

        self.save_button.draw(screen)
        self.back_button.draw(screen)
        self.name_text.draw(screen)
        if self.data is None:
            self.create_config_button.draw(screen)
