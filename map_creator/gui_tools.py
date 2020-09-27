import pygame

FONT = pygame.font.SysFont('calibre', 24)
# Default button images/ pygame .Surfaces.
IMAGE_NORMAL = pygame.Surface((100, 100))
IMAGE_NORMAL.fill(pygame.Color('dodgerblue1'))
IMAGE_HOVER = pygame.Surface((100, 100))
IMAGE_HOVER.fill(pygame.Color('lightskyblue'))
IMAGE_DOWN = pygame.Surface((100, 100))
IMAGE_DOWN.fill(pygame.Color('aquamarine1'))

color = {'black': (0, 0, 0), 'white': (255, 255, 255), 'red': (200, 0, 0), 'green': (0, 200, 0), 'blue': (0, 0, 200)}


class Button(pygame.sprite.Sprite):

    def set_image(self, image_normal=IMAGE_NORMAL, image_hover=IMAGE_HOVER, image_down=IMAGE_DOWN):
        self.image_normal_o = pygame.transform.scale(image_normal, (self.rect.width, self.rect.height))
        self.image_hover_o = pygame.transform.scale(image_hover, (self.rect.width, self.rect.height))
        self.image_down_o = pygame.transform.scale(image_down, (self.rect.width, self.rect.height))

        self.image_normal, self.image_hover, self.image_down = self.image_normal_o.copy(), self.image_hover_o.copy(), self.image_down_o.copy()

        self.image = self.image_normal

        self.move(self.rect.left, self.rect.top)

    def set_text(self, text, set_active_image=False):
        self.text = text
        self.move(self.rect.left, self.rect.top, set_active_image)

    def set_rect(self, x, y, w, h):
        self.image_normal_o = pygame.transform.scale(self.image_normal_o, (int(w), int(h)))
        self.image_hover_o = pygame.transform.scale(self.image_hover_o, (int(w), int(h)))
        self.image_down_o = pygame.transform.scale(self.image_down_o, (int(w), int(h)))

        self.move(x, y, True)

    def move(self, x, y, set_active_image=False):
        self.rect = self.image.get_rect(topleft=(x, y))
        # To center the text rect.
        image_center = self.image.get_rect().center
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=image_center)
        # original
        self.image_normal, self.image_hover, self.image_down = \
            self.image_normal_o.copy(), self.image_hover_o.copy(), self.image_down_o.copy()
        # Blit the text onto the images.
        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)

        if set_active_image:
            self.image = self.image_normal

    def __init__(self, x, y, width, height, callback=lambda: None,
                 font=FONT, text='', text_color=(0, 0, 0),
                 image_normal=IMAGE_NORMAL, image_hover=IMAGE_HOVER,
                 image_down=IMAGE_DOWN, fit_text=False, center=False):
        super().__init__()

        self.text = text
        self.font = font
        self.text_color = text_color

        if fit_text:
            f = font.render(text, True, text_color).get_rect()
            if f.width > width:
                width = f.width
            if f.height > height:
                height = f.height

        # original images
        self.image_normal_o = pygame.transform.scale(image_normal, (width, height))
        self.image_hover_o = pygame.transform.scale(image_hover, (width, height))
        self.image_down_o = pygame.transform.scale(image_down, (width, height))
        # Scale the images to the desired size (doesn't modify the originals).
        self.image_normal, self.image_hover, self.image_down = self.image_normal_o.copy(), self.image_hover_o.copy(), self.image_down_o.copy()

        self.image = self.image_normal  # The currently active image.
        if center:
            self.rect = self.image.get_rect(center=(x, y))
        else:
            self.rect = self.image.get_rect(topleft=(x, y))
        # To center the text rect.
        image_center = self.image.get_rect().center
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=image_center)
        # Blit the text onto the images.
        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)

        # This function will be called when the button gets pressed.
        self.callback = callback
        self.button_down = False
        self.selected = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and event.button == 1:
                self.image = self.image_down
                self.button_down = True
                self.callback()
        elif event.type == pygame.MOUSEBUTTONUP:
            # If the rect collides with the mouse pos.
            if self.rect.collidepoint(event.pos) and self.button_down:
                self.image = self.image_hover
            self.button_down = False
        elif event.type == pygame.MOUSEMOTION:
            collided = self.rect.collidepoint(event.pos)
            if collided and not self.button_down:
                self.image = self.image_hover
            elif not collided:
                self.image = self.image_normal

    def draw(self, screen):
        if self.selected:
            screen.blit(self.image_down, self.rect)
        else:
            screen.blit(self.image, self.rect)


class GuiContainer:
    min_scroll = 10
    scroll_offset = 0
    OBJ_MARGIN = 8
    max_scroll = 0

    def deselect_all(self):
        for obj in self.objects:
            obj.selected = False

    def click_obj(self, x):
        self.deselect_all()
        self.objects[x].selected = True
        self.callback(x-1)

    def __init__(self, objects, objects_size=(32, 32), callback=(lambda x=None: None),
                 rect=(0, 0, 100, 100), with_columns=True):
        self.with_columns = with_columns
        self.objects_size = objects_size
        self.rect = rect
        self.callback = callback
        self.cont = Button(0, 0, 100, 100)
        self.objects = []
        self.objects.append(Button(0, 0, objects_size[0], objects_size[1],
                                   text='#', callback=(lambda: self.click_obj(0))))
        for i in range(len(objects)):
            self.objects.append(Button(0, 0, objects_size[0], objects_size[1],
                                       image_normal=objects[i].image,
                                       image_down=objects[i].image_down,
                                       image_hover=objects[i].image_hover,
                                       callback=(lambda x=i: self.click_obj(x+1))))
        self.rebuild()

    def hits(self, pos):
        return self.rect[0] <= pos[0] <= self.rect[2] and self.rect[1] <= pos[1] <= self.rect[3]

    def set_rect(self, x, y, w, h):
        self.rect = (x, y, w, h)
        self.rebuild()

    def rebuild(self):

        if self.with_columns:
            cols = max(1, int((self.rect[2] - self.rect[0] - int(self.OBJ_MARGIN / 2))
                              / (self.objects_size[1] + self.OBJ_MARGIN)))
        else:
            cols = 1

        self.cont.set_rect(self.rect[0], self.rect[1], self.rect[2] - self.rect[0], self.rect[3] - self.rect[1])

        self.max_scroll = (int(len(self.objects) / cols) + 1) * (self.objects_size[1] + self.OBJ_MARGIN) - (self.rect[3] - self.rect[1])

        for i in range(len(self.objects)):
            self.objects[i].move(
                self.rect[0] + self.OBJ_MARGIN + ((self.objects_size[0] + self.OBJ_MARGIN) * (i % cols)),
                self.rect[1] + self.scroll_offset + int(i / cols) * (self.objects_size[1] + self.OBJ_MARGIN))

    def reset_scroll(self):
        self.scroll_offset = self.min_scroll
        self.rebuild()

    def handle_scroll(self, event):
        if not self.hits(event.pos):
            return False

        if event.button == 4:
            self.scroll_offset += 10
            if self.scroll_offset > self.min_scroll:
                self.scroll_offset = self.min_scroll
            self.rebuild()
        elif event.button == 5:
            if self.scroll_offset > -self.max_scroll:
                self.scroll_offset -= 10
                self.rebuild()
        return True

    def handle_event(self, event):
        for obj in self.objects:
            obj.handle_event(event)

    def draw(self, screen):
        self.cont.draw(screen)
        for obj in self.objects:
            obj.draw(screen)
