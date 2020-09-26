import math

import pygame
    
import json


class Map:
    TILE_SIZE = 16
    zoomed_tile_size = TILE_SIZE
    grid_d_size = TILE_SIZE

    tile_map = []
    object_map = []

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

        class MapDecoder(json.JSONDecoder):
            def decode(self2, s):
                result = super().decode(s)  # result = super(Decoder, self).decode(s) for Python 2.x
                return self2._decode(result)

            def _decode(self2, o):
                if isinstance(o, str):
                    return self.tile_manager.get_index(o)
                elif isinstance(o, dict):
                    return {k: self2._decode(v) for k, v in o.items()}
                elif isinstance(o, list):
                    return [self2._decode(v) for v in o]
                else:
                    return o

        self.tile_map = json.loads(line, cls=MapDecoder)

    def save(self):
        nmap = self.tile_map
        max_len = max([len(l) for l in self.tile_map])

        for y in self.tile_map:
            for _ in range(max_len - len(y)):
                y.append(0)

        namemap = []
        for y in range(len(nmap)):
            namemap.append([])
            for x in range(len(nmap[y])):
                namemap[y].append(self.tile_manager.tiles[nmap[y][x]].name)

        file = open(self.FILE, "w")
        file.write(json.dumps(namemap))
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
