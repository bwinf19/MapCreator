import math

import pygame
    
import json


class Map:
    TILE_SIZE = 16
    zoomed_tile_size = TILE_SIZE
    grid_d_size = TILE_SIZE

    tile_map = []
    object_map = []

    temp_object = -1
    temp_object_pos = (0, 0)

    offset_pos = (0, 0)

    show_grid = True

    FILE = "D:/JavaProgs/Mockmon/src/main/resources/map.json"

    def __init__(self, tm, om):
        self.tile_manager = tm
        self.object_manager = om
        self.drawable_tiles = []
        self.drawable_objects = []
        for tile in self.tile_manager.tiles:
            t = DrawableTile(tile.image)
            t.resize(self.zoomed_tile_size)
            self.drawable_tiles.append(t)

        for obj in self.object_manager.objects:
            t = DrawableObject(obj.image)
            t.resize(self.zoomed_tile_size/self.TILE_SIZE)
            self.drawable_objects.append(t)

        self.load()

    def load(self):
        file = open(self.FILE, "r")
        line = file.readline()
        file.close()

        try:
            loaded = json.loads(line)

            self.tile_map = [[self.tile_manager.get_index(x) for x in y] for y in loaded['tile_map']]
            self.object_map = [[self.object_manager.get_index(x) for x in y] for y in loaded['obj_map']]
        except KeyError or json.decoder.JSONDecodeError:
            pass
        except json.decoder.JSONDecodeError:
            pass

    def stringify_map(self, omap, managed_objs):
        max_len = max([0] + [len(l) for l in omap])

        for y in omap:
            for _ in range(max_len - len(y)):
                y.append(-1)

        namemap = []
        for y in range(len(omap)):
            namemap.append([])
            for x in range(len(omap[y])):
                if omap[y][x] == -1:
                    namemap[y].append('')
                else:
                    namemap[y].append(managed_objs[omap[y][x]].name)
        return namemap

    def save(self):

        file = open(self.FILE, "w")
        file.write(json.dumps({
            'tile_map': self.stringify_map(self.tile_map, self.tile_manager.tiles),
            'obj_map': self.stringify_map(self.object_map, self.object_manager.objects)
        }))
        file.close()
        print("saved")

    def set_tile(self, pos, tile_i, pen_size=1):
        if tile_i is None:
            return
        pen_size_off = pen_size-1
        xs = int(math.floor((pos[0]+self.offset_pos[0]) / self.zoomed_tile_size))
        ys = int(math.floor((pos[1]+self.offset_pos[1]) / self.zoomed_tile_size))

        while ys-pen_size_off < 0:
            self.tile_map = [[]] + self.tile_map
            self.offset_pos = (self.offset_pos[0], self.offset_pos[1] + self.zoomed_tile_size)
            ys += 1

        while xs-pen_size_off < 0:
            for y2 in range(len(self.tile_map)):
                self.tile_map[y2] = [0] + self.tile_map[y2]
            self.offset_pos = (self.offset_pos[0] + self.zoomed_tile_size, self.offset_pos[1])
            xs += 1

        for x in range(xs-pen_size_off, xs+pen_size_off+1):
            for y in range(ys-pen_size_off, ys+pen_size_off+1):
                while y > len(self.tile_map) - 1:
                    self.tile_map.append([])
                while x > len(self.tile_map[y]) - 1:
                    self.tile_map[y].append(-1)

                self.tile_map[y][x] = tile_i

    def set_object(self, pos, object_i):
        if object_i is None:
            return
        x = int(math.floor((pos[0] + self.offset_pos[0]) / self.zoomed_tile_size))
        y = int(math.floor((pos[1] + self.offset_pos[1]) / self.zoomed_tile_size))

        while y < 0:
            self.object_map = [[]] + self.object_map
            self.offset_pos = (self.offset_pos[0], self.offset_pos[1] + self.zoomed_tile_size)
            y += 1

        while x < 0:
            for y2 in range(len(self.object_map)):
                self.object_map[y2] = [0] + self.object_map[y2]
            self.offset_pos = (self.offset_pos[0] + self.zoomed_tile_size, self.offset_pos[1])
            x += 1

        while y > len(self.object_map) - 1:
            self.object_map.append([])
        while x > len(self.object_map[y]) - 1:
            self.object_map[y].append(-1)

        self.object_map[y][x] = object_i

    def show_temp_object(self, selected_object, pos=None):
        self.temp_object = -1 if selected_object is None else selected_object
        if selected_object != -1:
            self.temp_object_pos = pos

    def add_offset(self, x, y):
        self.offset_pos = (x, y)

    def zoom(self, x):
        self.offset_pos = (self.offset_pos[0]/self.zoomed_tile_size, self.offset_pos[1]/self.zoomed_tile_size)

        self.zoomed_tile_size = max(1, self.zoomed_tile_size+x)

        self.grid_d_size = self.zoomed_tile_size

        self.offset_pos = (int(self.offset_pos[0] * self.zoomed_tile_size), int(self.offset_pos[1] * self.zoomed_tile_size))

        for tile in self.drawable_tiles:
            tile.resize(self.zoomed_tile_size)

        for obj in self.drawable_objects:
            obj.resize(self.zoomed_tile_size/self.TILE_SIZE)

    def toggle_grid(self):
        self.show_grid = not self.show_grid

    def render(self, screen):
        screen.fill((0, 0, 0))

        for y in range(len(self.tile_map)):
            for x in range(len(self.tile_map[y])):
                if self.tile_map[y][x] != -1:
                    self.drawable_tiles[self.tile_map[y][x]]\
                        .draw(screen,
                              (x * self.zoomed_tile_size) - self.offset_pos[0],
                              (y * self.zoomed_tile_size) - self.offset_pos[1])

        for y in range(len(self.object_map)):
            for x in range(len(self.object_map[y])):
                if self.object_map[y][x] != -1:
                    self.drawable_objects[self.object_map[y][x]]\
                        .draw(screen,
                              (x * self.zoomed_tile_size) - self.offset_pos[0],
                              (y * self.zoomed_tile_size) - self.offset_pos[1])

        if self.temp_object != -1:
            x = int((self.temp_object_pos[0]-(self.temp_object_pos[0] % self.zoomed_tile_size))/self.zoomed_tile_size)
            y = int((self.temp_object_pos[1]-(self.temp_object_pos[1] % self.zoomed_tile_size))/self.zoomed_tile_size)
            self.drawable_objects[self.temp_object] \
                .draw(screen,
                      (x*self.zoomed_tile_size),
                      (y*self.zoomed_tile_size))

        if self.show_grid:
            y = -(self.offset_pos[1] % self.grid_d_size)
            while y < screen.get_height():
                pygame.draw.line(screen, (180, 180, 180), (0, y), (screen.get_width(), y), 1)
                y += self.grid_d_size

            x = -(self.offset_pos[0] % self.grid_d_size)
            while x < screen.get_width():
                pygame.draw.line(screen, (180, 180, 180), (x, 0), (x, screen.get_height()), 1)
                x += self.grid_d_size


class DrawableTile:
    def __init__(self, image):
        self.original_image = image
        self.image = self.original_image.copy()

    def resize(self, new_size):
        self.image = pygame.transform.scale(self.original_image, (new_size, new_size))

    def draw(self, screen, x, y):
        rect = self.image.get_rect(topleft=(x, y))
        screen.blit(self.image, rect)


class DrawableObject:
    def __init__(self, image):
        self.original_image = image
        self.image = self.original_image.copy()

    def resize(self, scale):
        self.image = pygame.transform.scale(
            self.original_image, (int(self.original_image.get_width()*scale), int(self.original_image.get_height()*scale)))

    def draw(self, screen, x, y):
        rect = self.image.get_rect(topleft=(x, y))
        screen.blit(self.image, rect)
