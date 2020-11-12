import pygame

from gui_tools import Button, GuiContainer, TextField, ObjectGuiContainer, IMAGE_GRAY

import os
import json


class ObjectGui:
    def __init__(self, gm, om):
        self.last_width = 500
        self.last_height = 500
        self.gm = gm

        self.object_manager = om

        self.object_index = None
        self.object = None
        self.name = 'ERROR! PLS ASK'
        self.data = None
        self.config = None

        self.bg = ObjectGuiContainer([], (32, 64), extras=[])

        self.back_button = Button(0, 0, 120, 30, text="Back", image_normal=IMAGE_GRAY,
                                  callback=self.gm.load_map)

        self.save_button = Button(0, 40, 120, 30, text="Save", image_normal=IMAGE_GRAY,
                                  callback=lambda: None)

        self.name_text = Button(140, 0, 180, 30, text=self.name)

        self.create_config_button = Button(140, 40, 1, 30, text=self.name)

        self.rebuild_scene(self.last_width, self.last_height)

    def entry(self):
        pass

    def exit(self):
        pass

    def set_object(self, x):
        self.object_index = x
        self.object = self.object_manager.objects[self.object_index]
        self.name = self.object.name

        self.name_text = Button(140, 0, 180, 30, text="Name: "+self.name, fit_text=True)

        self.config = os.path.join(self.object.path, 'config.json')

        if os.path.isfile(self.config):
            line = open(self.config, "r").readline()
            self.data = json.loads(line)
        else:
            self.data = None
            self.create_config_button = Button(140, 40, 1, 30, text='Create config.json for '+self.name,
                                               image_normal=IMAGE_GRAY, fit_text=True, callback=self.create_json)

    def create_json(self):
        self.save_json({'collision': False})
        self.set_object(self.object_index)

    def save_json(self, data):
        open(self.config, "w").write(json.dumps({
            'collision': str(data['collision']).lower(),
        }))
        print("saved")

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
