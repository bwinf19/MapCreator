import pygame

from gui_tools import Button, GuiContainer
from map import Map


class Gui:
    TILE_SIZE = 26
    OBJECTS_SIZE = 72

    cont_width = 200
    map_rect = [cont_width, 0, 100, 100]

    mouse_down = False
    scroll_pos = None

    pen_size = 1

    def clicked_tile(self, x):
        self.objects_cont.deselect_all()
        self.object_manager.selected_object = None
        self.tile_manager.selected_tile = x

    def clicked_object(self, x):
        self.tiles_cont.deselect_all()
        self.tile_manager.selected_tile = None
        self.object_manager.selected_object = x

    def __init__(self, tm, om, ma):
        self.tile_manager = tm
        self.object_manager = om

        self.map = ma

        self.buttons_cont = Button(0, 0, 40, 40)

        img = pygame.Surface((100, 100))
        img.fill((150, 150, 150))
        self.save_button = Button(0, 0, 80, 30, text="Save", callback=self.map.save, image_normal=img)
        self.grid_button = Button(0, 0, 80, 30, text="Grid", callback=self.map.toggle_grid, image_normal=img)
        self.pen_size_text = Button(0, 0, 120, 30, text="Pen Size: "+str(self.pen_size))
        self.pen_size_add = Button(0, 0, 35, 30, text="+", callback=self.add_pen_size, image_normal=img)
        self.pen_size_sub = Button(0, 0, 35, 30, text="-", callback=self.sub_pen_size, image_normal=img)

        self.tiles_cont = GuiContainer(self.tile_manager.tiles,
                                       (Gui.TILE_SIZE, Gui.TILE_SIZE), self.clicked_tile)

        self.objects_cont = GuiContainer(self.object_manager.objects,
                                         (Gui.OBJECTS_SIZE, Gui.OBJECTS_SIZE), self.clicked_object)

    def add_pen_size(self):
        self.pen_size += 1
        self.pen_size_text.set_text("Pen Size: "+str(self.pen_size), True)

    def sub_pen_size(self):
        if self.pen_size > 1:
            self.pen_size -= 1
            self.pen_size_text.set_text("Pen Size: "+str(self.pen_size), True)

    def rebuild_scene(self, width, height):
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

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.rebuild_scene(event.w, event.h)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.tiles_cont.handle_scroll(event):
                pass

            elif self.objects_cont.handle_scroll(event):
                pass

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
                    self.map.set_tile((event.pos[0] - self.map_rect[0], event.pos[1] - self.map_rect[1]),
                                      self.tile_manager.selected_tile, self.pen_size)
                    self.map.set_object((event.pos[0] - self.map_rect[0], event.pos[1] - self.map_rect[1]),
                                        self.object_manager.selected_object)

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
                self.map.show_temp_object(self.object_manager.selected_object,
                                          (event.pos[0]-self.map_rect[0], event.pos[1]-self.map_rect[1]))
                if self.mouse_down:
                    self.map.set_tile((event.pos[0]-self.map_rect[0], event.pos[1]-self.map_rect[1]),
                                      self.tile_manager.selected_tile, self.pen_size)
                if self.scroll_pos is not None:
                    self.map.add_offset(self.scroll_pos[0]-event.pos[0], self.scroll_pos[1]-event.pos[1])
            else:
                self.map.show_temp_object(-1)

        self.tiles_cont.handle_event(event)
        self.objects_cont.handle_event(event)

        self.save_button.handle_event(event)
        self.grid_button.handle_event(event)
        self.pen_size_add.handle_event(event)
        self.pen_size_sub.handle_event(event)

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
