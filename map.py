import math

import pygame
    
import json


class Map:
    TILE_SIZE = 16
    zoomed_tile_size = TILE_SIZE
    grid_d_size = TILE_SIZE

    wmap = []

    offset_pos = (0, 0)

    show_grid = True

    FILE = "D:/JavaProgs/Mockmon/src/main/resources/map.json"

    def __init__(self, tm):
        self.tile_manager = tm
        self.drawable_tiles = []
        for tile in self.tile_manager.tiles:
            t = DrawableTile(tile.image)
            t.resize(self.zoomed_tile_size)
            self.drawable_tiles.append(t)

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

        self.wmap = json.loads(line, cls=MapDecoder)

    def save(self):
        nmap = self.wmap
        max_len = max([len(l) for l in self.wmap])

        for y in self.wmap:
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
            self.wmap = [[]] + self.wmap
            self.offset_pos = (self.offset_pos[0], self.offset_pos[1] + self.zoomed_tile_size)
            ys += 1

        while xs-pen_size_off < 0:
            for y2 in range(len(self.wmap)):
                self.wmap[y2] = [0] + self.wmap[y2]
            self.offset_pos = (self.offset_pos[0] + self.zoomed_tile_size, self.offset_pos[1])
            xs += 1

        for x in range(xs-pen_size_off, xs+pen_size_off+1):
            for y in range(ys-pen_size_off, ys+pen_size_off+1):
                while y > len(self.wmap) - 1:
                    self.wmap.append([])
                while x > len(self.wmap[y]) - 1:
                    self.wmap[y].append(0)

                self.wmap[y][x] = tile_i

    def add_offset(self, x, y):
        self.offset_pos = (x, y)

    def zoom(self, x):
        self.offset_pos = (self.offset_pos[0]/self.zoomed_tile_size, self.offset_pos[1]/self.zoomed_tile_size)

        self.zoomed_tile_size = max(1, self.zoomed_tile_size+x)

        self.grid_d_size = self.zoomed_tile_size

        self.offset_pos = (int(self.offset_pos[0] * self.zoomed_tile_size), int(self.offset_pos[1] * self.zoomed_tile_size))

        for tile in self.drawable_tiles:
            tile.resize(self.zoomed_tile_size)

    def toggle_grid(self):
        self.show_grid = not self.show_grid

    def render(self, screen):
        screen.fill((0, 0, 0))

        for y in range(len(self.wmap)):
            for x in range(len(self.wmap[y])):
                if self.wmap[y][x] != -1:
                    self.drawable_tiles[self.wmap[y][x]]\
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
