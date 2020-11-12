import pygame

from gui_tools import Button, GuiContainer, TextField, ObjectGuiContainer, IMAGE_GRAY, EMPTY_MOUSE_EVENT

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


def rdist(p1, p2):
    return abs(abs(p1[0])-abs(p2[0])) + abs(abs(p1[1])-abs(p2[1]))


def resize_rect(rect, pos, size):
    ppos = (pos[0], size[1] - pos[1])

    if rdist(ppos, (rect[0], rect[1])) < rdist(ppos, (rect[0] + rect[2], rect[1] + rect[3])):
        dx = pos[0] - rect[0]
        dy = size[1] - pos[1] - rect[1]
        t = pos[0], size[1] - pos[1], rect[2] - dx, rect[3] - dy
    else:
        dx = pos[0] - rect[0]
        dy = size[1] - pos[1] - rect[1]
        t = rect[0], rect[1], dx, dy

    if t[0] < 0:
        t = 0, t[1], t[2]+t[0], t[3]
    elif t[0] >= size[0]:
        t = size[0]-1, t[1], t[2], t[3]
    if t[1] < 0:
        t = t[0], 0, t[2], t[3] + t[1]
    elif t[1] >= size[1]:
        t = t[0], size[1] - 1, t[2], t[3]
    if t[2] < 1:
        t = t[0], t[1], 1, t[3]
    elif t[2] > size[0]:
        t = t[0], t[1], size[0], t[3]
    if t[3] < 1:
        t = t[0], t[1], t[2], 1
    elif t[3] > size[1]:
        t = t[0], t[1], t[2], size[1]
    return t


def get_json(data):
    save_data = {'collision': str(data['collision']).lower()}
    if 'collision_box' in data and is_valid_rect(data['collision_box']):
        save_data['collision_box'] = save_rect(data['collision_box'])
    if 'trigger_box' in data and is_valid_rect(data['trigger_box']):
        save_data['trigger_box'] = save_rect(data['trigger_box'])
    if 'triggers' in data and data['triggers'] != '':
        save_data['triggers'] = data['triggers']
    return save_data


class ObjectGui:
    IMAGE_OFFSET = (240, 120)

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

        self.mouse_down = False

        self.setting_collision_box = False
        self.setting_trigger_box = False

        self.bg = ObjectGuiContainer([], (32, 64), extras=[])

        self.back_button = Button(0, 0, 120, 30, text="Back", image_normal=IMAGE_GRAY,
                                  callback=self.gm.load_map)

        self.save_button = Button(0, 40, 120, 30, text="Save", image_normal=IMAGE_GRAY,
                                  callback=self.save)

        self.name_text = Button(140, 0, 180, 30, text=self.name)

        self.create_config_button = Button(140, 40, 1, 30, text=self.name)

        self.collision_toggle_button = Button(140, 40, 100, 30,
                                              text=self.name, image_normal=IMAGE_GRAY, callback=self.toggle_collision)

        self.trigger_info_text = Button(240, 40, 100, 30, text='Trigger:')

        self.trigger_textfield = TextField(340, 40, 150, 30, text=self.name, change=self.update)

        self.set_collision_button = Button(0, 120, 200, 30, text='Edit collision box',
                                           image_normal=IMAGE_GRAY, callback=self.set_collision_box)

        self.set_trigger_box_button = Button(0, 160, 200, 30, text='Edit trigger box',
                                             image_normal=IMAGE_GRAY, callback=self.set_trigger_box)

        self.remove_collision_button = Button(0, 200, 200, 30, text='Remove collision box',
                                              image_normal=IMAGE_GRAY, callback=self.remove_collision_box)

        self.remove_trigger_box_button = Button(0, 240, 200, 30, text='Remove trigger box',
                                                image_normal=IMAGE_GRAY, callback=self.remove_trigger_box)

        self.json_info_text = Button(0, 30, 1, 30, text='')

        self.rebuild_scene(self.last_width, self.last_height)

    def entry(self):
        self.mouse_down = False

    def exit(self):
        self.mouse_down = False

    def collision_text(self):
        if self.data['collision']:
            return 'Collision On'
        else:
            return 'Collision Off'

    def toggle_collision(self):
        self.data['collision'] = not self.data['collision']
        self.update()

    def set_collision_box(self):
        self.setting_collision_box = True
        self.setting_trigger_box = False
        if not is_valid_rect(self.data['collision_box']):
            size = self.object.image.get_size()
            self.data['collision_box'] = 0, 0, size[0], size[1]
            self.update()

    def set_trigger_box(self):
        self.setting_collision_box = False
        self.setting_trigger_box = True
        if not is_valid_rect(self.data['trigger_box']):
            size = self.object.image.get_size()
            self.data['trigger_box'] = 0, 0, size[0], size[1]
            self.update()

    def remove_collision_box(self):
        self.data['collision_box'] = 0, 0, 0, 0
        self.setting_collision_box = False
        self.update()

    def remove_trigger_box(self):
        self.data['trigger_box'] = 0, 0, 0, 0
        self.setting_trigger_box = False
        self.update()

    def update(self):
        if self.data is not None:
            self.data['triggers'] = self.trigger_textfield.text
            self.collision_toggle_button.set_text(self.collision_text(), True)
            self.json_info_text.set_text(str(get_json(self.data)))
            self.rebuild_scene(self.last_width, self.last_height)

    def save(self):
        self.data['triggers'] = self.trigger_textfield.text
        self.save_json(self.data)

    def set_object(self, x):
        self.setting_collision_box = False
        self.setting_trigger_box = False

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
        open(self.config, "w").write(json.dumps(get_json(data)))
        print("saved")

    def rebuild_scene(self, width, height):
        self.last_width = width
        self.last_height = height
        self.bg.set_rect(0, 0, width, height)
        if self.data is not None:
            self.json_info_text = Button(0, height-30, 1, 30, text=str(get_json(self.data)), fit_text=True)

    def handle_resize_box(self, pos, buffer=30):
        size = self.object.image.get_size()
        if -buffer <= pos[0] <= size[0]+buffer and -buffer <= pos[1] <= size[1]+buffer:
            if self.setting_collision_box:
                self.data['collision_box'] = resize_rect(self.data['collision_box'], pos, size)
                self.update()
            elif self.setting_trigger_box:
                self.data['trigger_box'] = resize_rect(self.data['trigger_box'], pos, size)
                self.update()

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.rebuild_scene(event.w, event.h)
        self.save_button.handle_event(event)
        self.back_button.handle_event(event)
        if self.data is None:
            self.create_config_button.handle_event(event)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_down = True
                    self.handle_resize_box((event.pos[0] - self.IMAGE_OFFSET[0], event.pos[1] - self.IMAGE_OFFSET[1]))
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_down:
                    self.handle_resize_box((event.pos[0] - self.IMAGE_OFFSET[0], event.pos[1] - self.IMAGE_OFFSET[1]))
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_down = False

            if not self.setting_collision_box:
                self.set_collision_button.handle_event(event)
            else:
                self.set_collision_button.handle_event(EMPTY_MOUSE_EVENT)
            if not self.setting_trigger_box:
                self.set_trigger_box_button.handle_event(event)
            else:
                self.set_trigger_box_button.handle_event(EMPTY_MOUSE_EVENT)
            if is_valid_rect(self.data['collision_box']):
                self.remove_collision_button.handle_event(event)
            if is_valid_rect(self.data['trigger_box']):
                self.remove_trigger_box_button.handle_event(event)
            self.collision_toggle_button.handle_event(event)
            self.trigger_textfield.handle_event(event)

    def render(self, screen):
        self.bg.draw(screen)

        image_rect = self.object.image.get_rect(topleft=self.IMAGE_OFFSET)
        screen.blit(self.object.image, image_rect)

        self.save_button.draw(screen)
        self.back_button.draw(screen)
        self.name_text.draw(screen)
        self.trigger_info_text.draw(screen)
        if self.data is None:
            self.create_config_button.draw(screen)
        else:
            self.json_info_text.draw(screen)
            self.collision_toggle_button.draw(screen)
            self.trigger_textfield.draw(screen)
            if not self.setting_collision_box:
                self.set_collision_button.draw(screen)
            if not self.setting_trigger_box:
                self.set_trigger_box_button.draw(screen)
            if is_valid_rect(self.data['collision_box']):
                self.remove_collision_button.draw(screen)
                pygame.draw.rect(screen, (255, 0, 0), offset_rect(self.data['collision_box'], image_rect), 3)
            if is_valid_rect(self.data['trigger_box']):
                self.remove_trigger_box_button.draw(screen)
                pygame.draw.rect(screen, (0, 255, 0), offset_rect(self.data['trigger_box'], image_rect), 3)