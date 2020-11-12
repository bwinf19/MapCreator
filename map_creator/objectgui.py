import pygame

from gui_tools import Button, GuiContainer, TextField, ObjectGuiContainer, IMAGE_GRAY

import os
import json


def load_rect(rect):
    return [
        int(rect['x']),
        int(rect['y']),
        int(rect['w']),
        int(rect['h'])
    ]


def save_rect(rect):
    return {
        'x': str(rect[0]),
        'y': str(rect[1]),
        'w': str(rect[2]),
        'h': str(rect[3])
    }


def offset_rect(rect, off):
    return [
        off[0]+rect[0],
        off[1]+off[3]-rect[1]-rect[3],
        rect[2],
        rect[3]
    ]


def is_valid_rect(rect):
    return rect[2] > 0 and rect[3] > 0


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
                                  callback=self.save)

        self.name_text = Button(140, 0, 180, 30, text=self.name)

        self.create_config_button = Button(140, 40, 1, 30, text=self.name)

        self.collision_toggle_button = Button(140, 40, 100, 30,
                                              text=self.name, image_normal=IMAGE_GRAY, callback=self.toggle_collision)

        self.trigger_textfield = TextField(260, 40, 150, 30, text=self.name)

        self.rebuild_scene(self.last_width, self.last_height)

    def entry(self):
        pass

    def exit(self):
        pass

    def collision_text(self):
        if self.data['collision']:
            return 'Collision On'
        else:
            return 'Collision Off'

    def toggle_collision(self):
        self.data['collision'] = not self.data['collision']
        self.collision_toggle_button.set_text(self.collision_text(), True)

    def save(self):
        self.data['triggers'] = self.trigger_textfield.text
        self.save_json(self.data)

    def set_object(self, x):
        self.object_index = x
        self.object = self.object_manager.objects[self.object_index]
        self.name = self.object.name

        self.name_text = Button(140, 0, 1, 30, text="Name: "+self.name, fit_text=True)

        self.config = os.path.join(self.object.path, 'config.json')

        if os.path.isfile(self.config):
            line = open(self.config, "r").readline()
            loaded = json.loads(line)
            self.data = {'collision': loaded['collision'] == 'true'}
            if 'collision_box' in loaded:
                self.data['collision_box'] = load_rect(loaded['collision_box'])
            else:
                self.data['collision_box'] = 0, 0, 0, 0
            if 'trigger_box' in loaded:
                self.data['trigger_box'] = load_rect(loaded['trigger_box'])
            else:
                self.data['trigger_box'] = 0, 0, 0, 0
            if 'triggers' in loaded:
                self.data['triggers'] = loaded['triggers']
            else:
                self.data['triggers'] = ''

            self.collision_toggle_button.set_text(self.collision_text(), True)

            self.trigger_textfield.set_text(self.data['triggers'])

        else:
            self.data = None
            self.create_config_button = Button(140, 40, 1, 30, text='Create config.json for '+self.name,
                                               image_normal=IMAGE_GRAY, fit_text=True, callback=self.create_json)

    def create_json(self):
        self.save_json({'collision': False})
        self.set_object(self.object_index)

    def save_json(self, data):
        save_data = {'collision': str(data['collision']).lower()}
        if 'collision_box' in data and is_valid_rect(data['collision_box']):
            save_data['collision_box'] = save_rect(data['collision_box'])
        if 'trigger_box' in data and is_valid_rect(data['trigger_box']):
            save_data['trigger_box'] = save_rect(data['trigger_box'])
        if 'triggers' in data and data['triggers'] != '':
            save_data['triggers'] = data['triggers']
        print(save_data)
        open(self.config, "w").write(json.dumps(save_data))
        print("saved")

    def rebuild_scene(self, width, height):
        self.bg.set_rect(0, 0, width, height)

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.rebuild_scene(event.w, event.h)
        self.save_button.handle_event(event)
        self.back_button.handle_event(event)
        if self.data is None:
            self.create_config_button.handle_event(event)
        else:
            self.collision_toggle_button.handle_event(event)
            self.trigger_textfield.handle_event(event)

    def render(self, screen):
        self.bg.draw(screen)

        image = self.object.image
        image_rect = image.get_rect(topleft=(120, 100))
        screen.blit(image, image_rect)

        self.save_button.draw(screen)
        self.back_button.draw(screen)
        self.name_text.draw(screen)
        if self.data is None:
            self.create_config_button.draw(screen)
        else:
            self.collision_toggle_button.draw(screen)
            self.trigger_textfield.draw(screen)
            if is_valid_rect(self.data['collision_box']):
                pygame.draw.rect(screen, (255, 0, 0), offset_rect(self.data['collision_box'], image_rect), 3)
            if is_valid_rect(self.data['trigger_box']):
                pygame.draw.rect(screen, (0, 255, 0), offset_rect(self.data['trigger_box'], image_rect), 3)
