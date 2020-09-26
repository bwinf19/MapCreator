import pygame

from gui_tools import Button
from map import Map


class Gui:
    TILES_CONT_MIN = 10

    TILE_SIZE = 26
    TILE_SIZE_W_DIFF = 34

    last_width = 0
    last_height = 0

    cont_width = 200
    map_rect = [cont_width, 0, last_width-cont_width, last_height]

    mouse_down = False
    scroll_pos = None

    pen_size = 1

    def clicked_tile(self, x):
        for tile in self.tiles:
            tile.selected = False
        self.tiles[x].selected = True
        self.tile_manager.selected_tile = x

    def __init__(self, tm, om):
        self.tile_manager = tm
        self.object_manager = om

        self.map = Map(self.tile_manager)

        self.buttons_cont = Button(0, 0, 40, 40)

        img = pygame.Surface((100, 100))
        img.fill((150, 150, 150))
        self.save_button = Button(0, 0, 80, 30, text="Save", callback=self.map.save, image_normal=img)
        self.grid_button = Button(0, 0, 80, 30, text="Grid", callback=self.map.toggle_grid, image_normal=img)
        self.pen_size_text = Button(0, 0, 120, 30, text="Pen Size: "+str(self.pen_size))
        self.pen_size_add = Button(0, 0, 35, 30, text="+", callback=self.add_pen_size, image_normal=img)
        self.pen_size_sub = Button(0, 0, 35, 30, text="-", callback=self.sub_pen_size, image_normal=img)

        self.tiles_cont = Button(0, 0, self.cont_width, 200)
        self.objects_cont = Button(0, 0, self.cont_width, 200)

        self.tiles = []
        for i in range(len(self.tile_manager.tiles)):
            self.tiles.append(Button(0, 0, Gui.TILE_SIZE, Gui.TILE_SIZE,
                                     image_normal=self.tile_manager.tiles[i].image,
                                     image_down=self.tile_manager.tiles[i].image_down,
                                     image_hover=self.tile_manager.tiles[i].image_hover,
                                     callback=(lambda x=i: self.clicked_tile(x))))

        self.tiles_cont_offset = Gui.TILES_CONT_MIN

    def add_pen_size(self):
        self.pen_size += 1
        self.pen_size_text.set_text("Pen Size: "+str(self.pen_size), True)

    def sub_pen_size(self):
        if self.pen_size > 1:
            self.pen_size -= 1
            self.pen_size_text.set_text("Pen Size: "+str(self.pen_size), True)

    def rebuild_scene(self, width, height):
        if width != self.last_width or height != self.last_height:
            self.tiles_cont_offset = Gui.TILES_CONT_MIN
            self.last_width = width
            self.last_height = height

        self.cont_width = width/5

        self.tiles_cont.set_rect(0, 0, self.cont_width, height)
        self.objects_cont.set_rect(width-self.cont_width, 0, width, height)

        self.map_rect = [self.cont_width, 0, width-self.cont_width, height-40]

        self.buttons_cont.set_rect(self.cont_width, height-40, width, 40)

        self.save_button.move(self.cont_width+10, height-35)
        self.grid_button.move(self.cont_width+100, height-35)
        self.pen_size_text.move(self.cont_width+190, height-35)
        self.pen_size_add.move(self.cont_width+320, height-35)
        self.pen_size_sub.move(self.cont_width + 365, height - 35)

        cols = int((self.cont_width-5)/Gui.TILE_SIZE_W_DIFF)

        for i in range(len(self.tiles)):
            self.tiles[i].move(
                10+(Gui.TILE_SIZE_W_DIFF*(i % cols)),
                self.tiles_cont_offset+int(i/cols)*Gui.TILE_SIZE_W_DIFF)

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.rebuild_scene(event.w, event.h)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] <= self.cont_width:
                if event.button == 4:
                    self.tiles_cont_offset += 10
                    if self.tiles_cont_offset > Gui.TILES_CONT_MIN:
                        self.tiles_cont_offset = Gui.TILES_CONT_MIN
                    self.rebuild_scene(self.last_width, self.last_height)
                elif event.button == 5:
                    self.tiles_cont_offset -= 10
                    self.rebuild_scene(self.last_width, self.last_height)

            elif self.map_rect[0] < event.pos[0] < self.map_rect[2]\
                    and self.map_rect[1] < event.pos[1] < self.map_rect[3]:
                if event.button == 4:
                    self.map.zoom(1)
                elif event.button == 5:
                    self.map.zoom(-1)

            if event.button == 1:
                self.mouse_down = True
                if self.map_rect[0] < event.pos[0] < self.map_rect[2] \
                        and self.map_rect[1] < event.pos[1] < self.map_rect[3]:
                    self.map.set_tile((event.pos[0]-self.cont_width, event.pos[1]),
                                      self.tile_manager.selected_tile, self.pen_size)

            elif event.button == 3:
                self.scroll_pos = (event.pos[0]+self.map.offset_pos[0], event.pos[1]+self.map.offset_pos[1])

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_down = False
            elif event.button == 3:
                self.scroll_pos = None

        elif event.type == pygame.MOUSEMOTION:
            if self.map_rect[0] < event.pos[0] < self.map_rect[2] \
                    and self.map_rect[1] < event.pos[1] < self.map_rect[3]:
                if self.mouse_down:
                    self.map.set_tile((event.pos[0]-self.cont_width, event.pos[1]),
                                      self.tile_manager.selected_tile, self.pen_size)
                if self.scroll_pos is not None:
                    self.map.add_offset(self.scroll_pos[0]-event.pos[0], self.scroll_pos[1]-event.pos[1])

        self.save_button.handle_event(event)
        self.grid_button.handle_event(event)
        self.pen_size_add.handle_event(event)
        self.pen_size_sub.handle_event(event)
        for tile in self.tiles:
            tile.handle_event(event)

    def render(self, screen):
        map_screen = pygame.Surface((self.map_rect[2]-self.map_rect[0],
                                     self.map_rect[3]-self.map_rect[1]))
        self.map.render(map_screen)
        map_rect = map_screen.get_rect(topleft=(self.cont_width, 0))
        screen.blit(map_screen, map_rect)

        self.buttons_cont.draw(screen)

        self.save_button.draw(screen)
        self.grid_button.draw(screen)
        self.pen_size_text.draw(screen)
        self.pen_size_add.draw(screen)
        self.pen_size_sub.draw(screen)

        self.tiles_cont.draw(screen)
        self.objects_cont.draw(screen)
        for tile in self.tiles:
            tile.draw(screen)
