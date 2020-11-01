import pygame

from gui_tools import Button, ObjectGuiContainer


class NpcGui:
    def clicked_npc(self, x):
        self.npc_cont.select(x)
        self.npc_editor.npc['i'] = x

    def __init__(self, npce, npcm, gm):
        self.gm = gm
        self.npc_manager = npcm
        self.npc_editor = npce

        img = pygame.Surface((100, 100))
        img.fill((150, 150, 150))

        self.back_button = Button(0, 0, 120, 30, text="Cancel", image_normal=img,
                                  callback=lambda: self.gm.save_npc_and_load(self.npc_editor.pos,
                                                                             self.npc_editor.cnpc))

        self.save_button = Button(0, 40, 120, 30, text="Save", image_normal=img,
                                  callback=lambda: self.gm.save_npc_and_load(self.npc_editor.pos,
                                                                             self.npc_editor.npc))

        self.bg = ObjectGuiContainer([], (32, 64), extras=[])

        self.npc_cont = ObjectGuiContainer(self.npc_manager.npcs, (32, 64),
                                           extras=[], callback=self.clicked_npc,
                                           with_columns=False, horizontal=True)

    def entry(self):
        self.clicked_npc(self.npc_editor.npc['i'])

    def rebuild_scene(self, width, height):
        self.bg.set_rect(0, 0, width, height)
        self.npc_cont.set_rect(120, 0, width, 100)

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.rebuild_scene(event.w, event.h)
        self.back_button.handle_event(event)
        self.save_button.handle_event(event)
        self.npc_cont.handle_event(event)

    def render(self, screen):
        self.bg.draw(screen)
        self.back_button.draw(screen)
        self.save_button.draw(screen)
        self.npc_cont.draw(screen)
