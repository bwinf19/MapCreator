import pygame

pygame.init()

FONT = pygame.font.SysFont('Calibre', 24)
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
        self.image_normal, self.image_hover, self.image_down =\
            self.image_normal_o.copy(), self.image_hover_o.copy(), self.image_down_o.copy()
        # Blit the text onto the images.
        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)

        if set_active_image:
            self.image = self.image_normal

    def __init__(self, x, y, width, height, callback=lambda: next,
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
