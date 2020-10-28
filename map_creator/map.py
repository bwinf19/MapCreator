import math

import pygame
    
import json


class Map:
    TILE_SIZE = 32
    LINE_COLOR = (180, 180, 180)
    zoomed_tile_size = TILE_SIZE
    grid_d_size = TILE_SIZE

    spawn_point = (0, 0)

    tile_map = []

    object_map = []

    npc_map = {}

    temp_object = -1
    temp_object_pos = (0, 0)

    offset_pos = (0, 0)

    show_grid = True

    def grid_pos(self, pos):
        x = int(math.floor((pos[0] + self.offset_pos[0]) / self.zoomed_tile_size))
        y = int(math.floor((pos[1] + self.offset_pos[1]) / self.zoomed_tile_size))
        return x, y

    def ungrid_pos(self, pos):
        x = (pos[0] * self.zoomed_tile_size) - self.offset_pos[0]
        y = (pos[1] * self.zoomed_tile_size) - self.offset_pos[1]
        return x, y

    def grid_object(self, pos, image):
        x = int((pos[0] + self.offset_pos[0]) / self.zoomed_tile_size)
        y = pos[1] + self.offset_pos[1] - image.get_height()
        y = int(y / self.zoomed_tile_size) + 1
        return x, y

    def ungrid_object(self, pos, obj_i):
        x = (pos[0] * self.zoomed_tile_size) - self.offset_pos[0]
        y = (pos[1] + 1) * self.zoomed_tile_size - self.drawable_objects[obj_i].image.get_height() - self.offset_pos[1]
        return x, y

    def __init__(self, tm, om, trm, file):
        self.file = file
        self.tile_manager = tm
        self.object_manager = om
        self.npc_manager = trm

        self.sp_image = DrawableSpImage(pygame.image.load("sp.png"))
        self.sp_image.resize(self.zoomed_tile_size)

        self.drawable_tiles = []
        self.drawable_objects = []
        self.drawable_npcs = []
        for tile in self.tile_manager.tiles:
            t = DrawableTile(tile.image)
            t.resize(self.zoomed_tile_size)
            self.drawable_tiles.append(t)

        for obj in self.object_manager.objects:
            t = DrawableObject(obj.image)
            t.resize(self.zoomed_tile_size/self.TILE_SIZE)
            self.drawable_objects.append(t)

        for tr in self.npc_manager.npcs:
            t = DrawableObject(tr.image)
            t.resize(self.zoomed_tile_size/self.TILE_SIZE)
            self.drawable_npcs.append(t)

        self.load()

    def load(self):

        try:
            file = open(self.file, "r")
            line = file.readline()
            file.close()

            loaded = json.loads(line)

            self.spawn_point = (int(loaded['spawn_point']['x']), int(loaded['spawn_point']['y']))
            self.tile_map = [[self.tile_manager.get_index(x) for x in y] for y in loaded['tile_map']]
            self.object_map = [[self.object_manager.get_index(x) for x in y] for y in loaded['obj_map']]
            self.npc_map = {(int(v['x']), int(v['y'])): self.npc_manager.get_index(v['type']) for v in loaded['npcs']}

        except KeyError:
            pass
        except json.decoder.JSONDecodeError:
            pass
        except FileNotFoundError:
            pass

    def stringify_list(self, omap, managed_objs):
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

    def stringify_dict(self, odict, managed_objs):
        nlist = []
        for k, v in odict.items():
            nlist.append({'x': int(k[0]), 'y': int(k[1]), 'type': managed_objs[v].name})
        return nlist

    def save(self):

        file = open(self.file, "w")
        file.write(json.dumps({
            'spawn_point': {'x': str(self.spawn_point[0]), 'y': str(self.spawn_point[1])},
            'tile_map': self.stringify_list(self.tile_map, self.tile_manager.tiles),
            'obj_map': self.stringify_list(self.object_map, self.object_manager.objects),
            'npcs': self.stringify_dict(self.npc_map, self.npc_manager.npcs)
        }))
        file.close()
        print("saved")

    def expand(self, x, y):
        while y < 0:
            self.tile_map = [[]] + self.tile_map
            self.object_map = [[]] + self.object_map
            self.offset_pos = (self.offset_pos[0], self.offset_pos[1] + self.zoomed_tile_size)
            self.spawn_point = self.spawn_point[0], self.spawn_point[1] + 1
            y += 1

        while x < 0:
            for y2 in range(len(self.tile_map)):
                self.tile_map[y2] = [-1] + self.tile_map[y2]
            for y2 in range(len(self.object_map)):
                self.object_map[y2] = [-1] + self.object_map[y2]
            self.offset_pos = (self.offset_pos[0] + self.zoomed_tile_size, self.offset_pos[1])
            self.spawn_point = self.spawn_point[0] + 1, self.spawn_point[1]
            x += 1

    def set_tile(self, pos, tile_i, pen_size=1):
        if tile_i is None:
            return
        pen_size_off = pen_size-1
        xs, ys = self.grid_pos(pos)

        self.expand(xs-pen_size_off, ys-pen_size_off)

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
        x, y = self.grid_pos(pos)

        self.expand(x, y)

        while y > len(self.object_map) - 1:
            self.object_map.append([])
        while x > len(self.object_map[y]) - 1:
            self.object_map[y].append(-1)

        self.object_map[y][x] = object_i

    def set_npc(self, pos, npc_i):
        if npc_i == -1:
            del self.npc_map[self.grid_pos(pos)]
        else:
            self.npc_map[self.grid_pos(pos)] = npc_i

    def set_spawn_point(self, pos):
        self.spawn_point = self.grid_pos(pos)

    def show_temp_object(self, selected_object, pos=None):
        self.temp_object = -1 if selected_object is None else selected_object
        if selected_object != -1:
            self.temp_object_pos = pos
            
    def add_offset(self, x, y):
        self.offset_pos = (x, y)

    def zoom(self, x):
        self.offset_pos = (self.offset_pos[0]/self.zoomed_tile_size, self.offset_pos[1]/self.zoomed_tile_size)

        self.zoomed_tile_size = max(4, self.zoomed_tile_size+x)

        self.grid_d_size = self.zoomed_tile_size

        self.offset_pos = (int(self.offset_pos[0] * self.zoomed_tile_size), int(self.offset_pos[1] * self.zoomed_tile_size))

        for tile in self.drawable_tiles:
            tile.resize(self.zoomed_tile_size)

        for obj in self.drawable_objects+self.drawable_npcs:
            obj.resize(self.zoomed_tile_size/self.TILE_SIZE)

        self.sp_image.resize(self.zoomed_tile_size)

    def toggle_grid(self):
        self.show_grid = not self.show_grid

    def render(self, screen):
        screen.fill((0, 0, 0))

        y = -(self.offset_pos[1] % self.zoomed_tile_size)
        while y < screen.get_height():
            x = -(self.offset_pos[0] % self.zoomed_tile_size)
            while x < screen.get_width():
                xa, ya = self.grid_pos((x, y))
                if 0 <= xa and 0 <= ya:
                    try:
                        ti = self.tile_map[ya][xa]
                        if ti != -1:
                            self.drawable_tiles[ti].draw(screen, x, y)
                    except IndexError:
                        pass
                x += self.zoomed_tile_size
            y += self.zoomed_tile_size

        temp_obj_grid_pos = self.grid_pos(self.temp_object_pos)
        drawn_temp_obj = False

        y = -(self.offset_pos[1] % self.zoomed_tile_size)
        while y < screen.get_height():
            x = -(self.offset_pos[0] % self.zoomed_tile_size)
            while x < screen.get_width():
                xa, ya = self.grid_pos((x, y))
                if 0 <= xa and 0 <= ya:
                    try:
                        oi = self.object_map[ya][xa]
                        if oi != -1:
                            obj = self.drawable_objects[oi]
                            pos = self.ungrid_pos(self.grid_object((x, y), obj.image))
                            obj.draw(screen, pos[0], pos[1])
                    except IndexError:
                        pass
                    if (xa, ya) in self.npc_map:
                        trainer = self.drawable_npcs[self.npc_map[(xa, ya)]]
                        pos = self.ungrid_pos(self.grid_object((x, y), trainer.image))
                        trainer.draw(screen, pos[0], pos[1])
                    if self.temp_object != -1 and (xa, ya) == temp_obj_grid_pos:
                        obj = self.drawable_objects[self.temp_object]
                        pos = self.ungrid_pos(self.grid_object((x, y), obj.image))
                        obj.draw(screen, pos[0], pos[1])
                        drawn_temp_obj = True
                x += self.zoomed_tile_size
            y += self.zoomed_tile_size

        if (not drawn_temp_obj) and self.temp_object != -1:
            x, y = self.ungrid_object(temp_obj_grid_pos, self.temp_object)
            self.drawable_objects[self.temp_object].draw(screen, x, y)

        if self.show_grid:
            y = -(self.offset_pos[1] % self.grid_d_size)
            while y < screen.get_height():
                pygame.draw.line(screen, self.LINE_COLOR, (0, y), (screen.get_width(), y), 1)
                y += self.grid_d_size

            x = -(self.offset_pos[0] % self.grid_d_size)
            while x < screen.get_width():
                pygame.draw.line(screen, self.LINE_COLOR, (x, 0), (x, screen.get_height()), 1)
                x += self.grid_d_size

        pos = self.ungrid_pos(self.spawn_point)
        self.sp_image.draw(screen, pos[0], pos[1])


class DrawableSpImage:
    def __init__(self, image):
        self.original_image = image
        self.image = self.original_image.copy()

    def resize(self, new_size):
        self.image = pygame.transform.scale(self.original_image, (new_size, new_size))

    def draw(self, screen, x, y):
        rect = self.image.get_rect(topleft=(x, y))
        screen.blit(self.image, rect)


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
