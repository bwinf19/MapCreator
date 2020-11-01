import pygame

from gui_tools import Button, GuiContainer, ObjectGuiContainer, IMAGE_NORMAL


class Gui:
    TILE_SIZE = 34
    OBJECTS_SIZE = 72
    TRAINERS_SIZE = 50

    cont_width = 200
    map_rect = [cont_width, 0, 100, 100]

    mouse_down = False
    scroll_pos = None

    pen_size = 1

    setting_spawn_point = False

    def deselect_all(self):
        self.tiles_cont.deselect_all()
        self.npc_cont.deselect_all()
        self.objects_cont.deselect_all()
        self.tile_manager.selected_tile = None
        self.npc_manager.selected_npc = None
        self.object_manager.selected_object = None

    def clicked_tile(self, x):
        self.deselect_all()
        self.tiles_cont.select(x)
        self.tile_manager.selected_tile = x

    def clicked_object(self, x):
        self.deselect_all()
        self.objects_cont.select(x)
        self.object_manager.selected_object = x

    def clicked_npc(self, x):
        self.deselect_all()
        self.npc_cont.select(x)
        self.npc_manager.selected_npc = x

    def set_spawn_point(self):
        self.clicked_object(None)
        self.clicked_tile(None)
        self.setting_spawn_point = True

    def __init__(self, tm, om, trm, mm):
        self.tile_manager = tm
        self.object_manager = om
        self.npc_manager = trm

        self.map_manager = mm

        img = pygame.Surface((100, 100))
        img.fill((150, 150, 150))

        self.pen_size_text = Button(0, 0, 120, 30, text="Pen Size: " + str(self.pen_size),
                                    image_hover=IMAGE_NORMAL, image_down=IMAGE_NORMAL)

        buttons = [
            Button(0, 0, 80, 30, text="Save", callback=self.map_manager.save, image_normal=img),
            Button(0, 0, 80, 30, text="Set SP", callback=self.set_spawn_point, image_normal=img),
            Button(0, 0, 80, 30, text="Grid", callback=self.map_manager.toggle_grid, image_normal=img),
            self.pen_size_text,
            Button(0, 0, 35, 30, text="+", callback=self.add_pen_size, image_normal=img),
            Button(0, 0, 35, 30, text="-", callback=self.sub_pen_size, image_normal=img)
        ]

        buttons += [Button(0, 0, 100, 30, text=str(ma),
                           callback=lambda x=ma: self.map_manager.select_map(x), image_normal=img)
                    for ma in self.map_manager.maps.keys()]

        self.buttons_cont = GuiContainer(buttons, horizontal=True, with_columns=False)

        self.tiles_cont = ObjectGuiContainer(self.tile_manager.tiles,
                                             (Gui.TILE_SIZE, Gui.TILE_SIZE), self.clicked_tile)

        self.npc_cont = ObjectGuiContainer(self.npc_manager.npcs,
                                           (Gui.TRAINERS_SIZE, Gui.TRAINERS_SIZE), self.clicked_npc)

        self.objects_cont = ObjectGuiContainer(self.object_manager.objects,
                                               (Gui.OBJECTS_SIZE, Gui.OBJECTS_SIZE), self.clicked_object)

    def add_pen_size(self):
        self.pen_size += 1
        self.pen_size_text.set_text("Pen Size: " + str(self.pen_size), True)

    def sub_pen_size(self):
        if self.pen_size > 1:
            self.pen_size -= 1
            self.pen_size_text.set_text("Pen Size: " + str(self.pen_size), True)

    def rebuild_scene(self, width, height):
        self.cont_width = width / 5

        self.tiles_cont.set_rect(0, 0, self.cont_width, height / 2)
        self.npc_cont.set_rect(0, height / 2, self.cont_width, height)
        self.objects_cont.set_rect(width - self.cont_width, 0, width, height)

        self.map_rect = [self.cont_width, 0, width - self.cont_width, height - 40]

        self.buttons_cont.set_rect(self.cont_width, height - 40, width, height)

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.rebuild_scene(event.w, event.h)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.tiles_cont.handle_scroll(event):
                pass

            elif self.objects_cont.handle_scroll(event):
                pass

            elif self.buttons_cont.handle_scroll(event):
                pass

            elif self.npc_cont.handle_scroll(event):
                pass

            elif self.map_rect[0] < event.pos[0] < self.map_rect[2] \
                    and self.map_rect[1] < event.pos[1] < self.map_rect[3]:
                if event.button == 4:
                    self.map_manager.current_map.zoom(1)
                elif event.button == 5:
                    self.map_manager.current_map.zoom(-1)

            if event.button == 1:
                self.mouse_down = True
                if self.map_rect[0] < event.pos[0] < self.map_rect[2] \
                        and self.map_rect[1] < event.pos[1] < self.map_rect[3]:
                    if self.setting_spawn_point:
                        self.setting_spawn_point = False
                        self.map_manager.current_map.set_spawn_point((event.pos[0] - self.map_rect[0],
                                                                      event.pos[1] - self.map_rect[1]))
                    else:
                        self.map_manager.current_map.set_tile((event.pos[0] - self.map_rect[0],
                                                               event.pos[1] - self.map_rect[1]),
                                                              self.tile_manager.selected_tile, self.pen_size)
                        self.map_manager.current_map.set_object((event.pos[0] - self.map_rect[0],
                                                                 event.pos[1] - self.map_rect[1]),
                                                                self.object_manager.selected_object)
                        self.map_manager.current_map.set_npc((event.pos[0] - self.map_rect[0],
                                                              event.pos[1] - self.map_rect[1]),
                                                             self.npc_manager.selected_npc)

            elif event.button == 3:
                self.scroll_pos = (event.pos[0] + self.map_manager.current_map.offset_pos[0],
                                   event.pos[1] + self.map_manager.current_map.offset_pos[1])

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_down = False
            elif event.button == 3:
                self.scroll_pos = None

        elif event.type == pygame.MOUSEMOTION:
            if self.map_rect[0] < event.pos[0] < self.map_rect[2] \
                    and self.map_rect[1] < event.pos[1] < self.map_rect[3]:
                self.map_manager.current_map.show_temp_object(self.object_manager.selected_object,
                                                              (event.pos[0] - self.map_rect[0],
                                                               event.pos[1] - self.map_rect[1]))
                if self.mouse_down:
                    self.map_manager.current_map.set_tile((event.pos[0] - self.map_rect[0],
                                                           event.pos[1] - self.map_rect[1]),
                                                          self.tile_manager.selected_tile, self.pen_size)
                    self.map_manager.current_map.set_object((event.pos[0] - self.map_rect[0],
                                                             event.pos[1] - self.map_rect[1]),
                                                            self.object_manager.selected_object)
                    self.map_manager.current_map.set_npc((event.pos[0] - self.map_rect[0],
                                                          event.pos[1] - self.map_rect[1]),
                                                         self.npc_manager.selected_npc)
                if self.scroll_pos is not None:
                    self.map_manager.current_map.add_offset(self.scroll_pos[0] - event.pos[0],
                                                            self.scroll_pos[1] - event.pos[1])
            else:
                self.map_manager.current_map.show_temp_object(-1)

        self.tiles_cont.handle_event(event)
        self.npc_cont.handle_event(event)
        self.objects_cont.handle_event(event)
        self.buttons_cont.handle_event(event)

    def render(self, screen):
        map_screen = pygame.Surface((self.map_rect[2] - self.map_rect[0],
                                     self.map_rect[3] - self.map_rect[1]))
        self.map_manager.current_map.render(map_screen)
        map_rect = map_screen.get_rect(topleft=(self.cont_width, 0))
        screen.blit(map_screen, map_rect)

        self.buttons_cont.draw(screen)
        self.tiles_cont.draw(screen)
        self.npc_cont.draw(screen)
        self.objects_cont.draw(screen)
