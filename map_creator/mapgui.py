import pygame

from gui_tools import Button, GuiContainer, ObjectGuiContainer, IMAGE_NORMAL, IMAGE_DOWN, IMAGE_GRAY, ICON_ERASER, \
    ICON_CURSOR, ICON_ROT_LEFT, ICON_ROT_RIGHT


class MapGui:
    TILE_SIZE = 34
    OBJECTS_SIZE = 72
    TRAINERS_SIZE = 50

    cont_width = 200
    map_rect = [cont_width, 40, 100, 100]

    mouse_down = False
    scroll_pos = None

    pen_size = 1

    setting_spawn_point = False

    copying = False

    def deselect_all(self):
        self.tiles_cont.deselect_all()
        self.npc_cont.deselect_all()
        self.objects_cont.deselect_all()
        self.tile_manager.selected_tile = None
        self.npc_manager.selected_npc = None
        self.object_manager.selected_object = None

    def clicked_tile(self, x):
        self.stop_copy()
        self.deselect_all()
        self.tiles_cont.select(x)
        self.tile_manager.selected_tile = x

    def clicked_object(self, x):
        self.stop_copy()
        self.deselect_all()
        self.objects_cont.select(x)
        self.object_manager.selected_object = x

    def clicked_npc(self, x):
        self.stop_copy()
        self.deselect_all()
        self.npc_cont.select(x)
        self.npc_manager.selected_npc = x

    def set_spawn_point(self):
        self.clicked_object(None)
        self.clicked_tile(None)
        self.setting_spawn_point = True

    def toggle_grid(self):
        self.map_manager.current_map.toggle_grid()

    def update_show_names(self):
        self.map_manager.current_map.set_object_names(self.show_names)
        i = 0
        for node in self.objects_cont.nodes[self.objects_cont.click_offset:]:
            if self.show_names:
                node.set_text(self.object_manager.objects[i].name, True, fit_rect=True, alpha=128)
            else:
                node.set_text('', True)
            i += 1

    def toggle_names(self):
        self.show_names = not self.show_names
        self.update_show_names()

    def load_object(self, x):
        if x >= 0:
            self.map_manager.gm.load_object(x)

    def refresh(self):
        self.map_manager.refresh()
        buttons = []
        for ma in self.map_manager.maps.keys():
            if ma == self.map_manager.current_name:
                buttons.append(Button(0, 0, 100, 30, text=str(ma), image_normal=IMAGE_DOWN, fit_text=True))
            else:
                buttons.append(Button(0, 0, 100, 30, text=str(ma),
                                      callback=lambda x=ma: (self.map_manager.select_map(x), self.entry()),
                                      image_normal=IMAGE_GRAY, fit_text=True))

        self.buttons_cont_top = GuiContainer(buttons, horizontal=True, with_columns=False)

        self.object_manager.refresh()
        self.objects_cont = ObjectGuiContainer(self.object_manager.objects, (MapGui.OBJECTS_SIZE, MapGui.OBJECTS_SIZE),
                                               self.clicked_object, callback_left=self.load_object)

        self.update_show_names()

    def __init__(self, tm, om, trm, mm):
        self.last_width = None
        self.last_height = None

        self.show_names = False

        self.tile_manager = tm
        self.object_manager = om
        self.npc_manager = trm

        self.map_manager = mm

        self.pen_size_text = Button(0, 0, 120, 30, text="Pen Size: " + str(self.pen_size),
                                    image_hover=IMAGE_NORMAL, image_down=IMAGE_NORMAL)

        self.copy_button = Button(0, 0, 80, 30, text="Copy", callback=self.set_copy, image_normal=IMAGE_GRAY)

        self.buttons_cont_top = None

        self.buttons_cont_bot = GuiContainer([
            Button(0, 0, 80, 30, text="Save", callback=self.map_manager.save, image_normal=IMAGE_GRAY),
            Button(0, 0, 80, 30, text="Set SP", callback=self.set_spawn_point, image_normal=IMAGE_GRAY),
            Button(0, 0, 80, 30, text="Grid", callback=self.toggle_grid, image_normal=IMAGE_GRAY),
            Button(0, 0, 80, 30, text="Names", callback=self.toggle_names, image_normal=IMAGE_GRAY),
            self.pen_size_text,
            Button(0, 0, 35, 30, text="+", callback=self.add_pen_size, image_normal=IMAGE_GRAY),
            Button(0, 0, 35, 30, text="-", callback=self.sub_pen_size, image_normal=IMAGE_GRAY),
            self.copy_button
        ], horizontal=True, with_columns=False)

        self.tiles_cont = ObjectGuiContainer(self.tile_manager.tiles,
                                             (MapGui.TILE_SIZE, MapGui.TILE_SIZE), self.clicked_tile)

        self.npc_cont = ObjectGuiContainer(self.npc_manager.npcs, (MapGui.TRAINERS_SIZE, MapGui.TRAINERS_SIZE),
                                           self.clicked_npc,
                                           extras=[ICON_ERASER, ICON_CURSOR, ICON_ROT_LEFT, ICON_ROT_RIGHT])

        self.objects_cont = None
        self.refresh()

    def entry(self):
        self.refresh()
        if self.last_width is not None:
            self.rebuild_scene(self.last_width, self.last_height)
        self.map_manager.set_current_map()

    def exit(self):
        self.map_manager.save()
        self.mouse_down = False
        self.scroll_pos = None
        self.deselect_all()

    def add_pen_size(self):
        self.pen_size += 1
        self.pen_size_text.set_text("Pen Size: " + str(self.pen_size), True)

    def sub_pen_size(self):
        if self.pen_size > 1:
            self.pen_size -= 1
            self.pen_size_text.set_text("Pen Size: " + str(self.pen_size), True)

    def set_copy(self):
        if not self.copying:
            self.deselect_all()
            self.copying = True
            self.copy_button.set_text('Copying')
            self.copy_button.image_normal = self.copy_button.image_hover
        else:
            self.stop_copy()

    def stop_copy(self):
        self.copying = False
        self.map_manager.current_map.reset_copy()
        self.copy_button.image_normal = self.copy_button.image_normal_o
        self.copy_button.set_text('Copy')

    def rebuild_scene(self, width, height):
        self.last_width = width
        self.last_height = height
        self.cont_width = width / 5

        self.tiles_cont.set_rect(0, 0, self.cont_width, height / 2)
        self.npc_cont.set_rect(0, height / 2, self.cont_width, height)
        self.objects_cont.set_rect(width - self.cont_width, 0, width, height)

        self.map_rect = [self.cont_width, 40, width - self.cont_width, height - 40]

        self.buttons_cont_top.set_rect(self.cont_width, 0, width - self.cont_width + 5, 40)

        self.buttons_cont_bot.set_rect(self.cont_width, height - 40, width - self.cont_width + 5, height)

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.rebuild_scene(event.w, event.h)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.tiles_cont.handle_scroll(event):
                pass

            elif self.objects_cont.handle_scroll(event):
                pass

            elif self.buttons_cont_top.handle_scroll(event):
                pass

            elif self.buttons_cont_bot.handle_scroll(event):
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
                    elif self.copying:
                        self.map_manager.current_map.set_copy((event.pos[0] - self.map_rect[0],
                                                               event.pos[1] - self.map_rect[1]),
                                                              self.pen_size)
                    else:
                        self.map_manager.current_map.set_tile((event.pos[0] - self.map_rect[0],
                                                               event.pos[1] - self.map_rect[1]),
                                                              self.tile_manager.selected_tile, self.pen_size)
                        self.map_manager.current_map.set_object((event.pos[0] - self.map_rect[0],
                                                                 event.pos[1] - self.map_rect[1]),
                                                                self.object_manager.selected_object, self.pen_size)
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
                if not self.copying:
                    self.map_manager.current_map.show_temp_object(self.object_manager.selected_object,
                                                                  (event.pos[0] - self.map_rect[0],
                                                                   event.pos[1] - self.map_rect[1]),
                                                                  self.pen_size)
                if self.mouse_down:
                    if self.copying:
                        self.map_manager.current_map.set_copy((event.pos[0] - self.map_rect[0],
                                                               event.pos[1] - self.map_rect[1]),
                                                              self.pen_size)
                    else:
                        self.map_manager.current_map.set_tile((event.pos[0] - self.map_rect[0],
                                                               event.pos[1] - self.map_rect[1]),
                                                              self.tile_manager.selected_tile,
                                                              self.pen_size)
                        self.map_manager.current_map.set_object((event.pos[0] - self.map_rect[0],
                                                                 event.pos[1] - self.map_rect[1]),
                                                                self.object_manager.selected_object,
                                                                self.pen_size)
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
        self.buttons_cont_top.handle_event(event)
        self.buttons_cont_bot.handle_event(event)

    def render(self, screen):
        map_screen = pygame.Surface((self.map_rect[2] - self.map_rect[0],
                                     self.map_rect[3] - self.map_rect[1]))
        self.map_manager.current_map.render(map_screen)
        map_rect = map_screen.get_rect(topleft=(self.cont_width, 40))
        screen.blit(map_screen, map_rect)

        self.buttons_cont_top.draw(screen)
        self.buttons_cont_bot.draw(screen)
        self.tiles_cont.draw(screen)
        self.npc_cont.draw(screen)
        self.objects_cont.draw(screen)
