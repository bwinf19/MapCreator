import pygame

from gui_tools import Button, ObjectGuiContainer, GuiContainer, TextField


class NpcGui:
    def clicked_npc(self, x):
        self.npc_cont.select(x)
        self.npc_editor.npc['i'] = x

    def __init__(self, npce, npcm, gm):
        self.last_width = 500
        self.last_height = 500
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

        self.dialog_info_text = Button(0, 100, 130, 35, text='Dialog Lines')
        self.dialog_options = GuiContainer([Button(0, 0, 35, 35, text='+', image_normal=img, callback=self.add_dialog),
                                            Button(0, 0, 35, 35, text='-', image_normal=img, callback=self.sub_dialog)], care_size=False)
        self.dialog_options.set_rect(0, 0, 100, 35)

        self.pokemon_info_text = GuiContainer([Button(0, 0, 100, 35, text='Poke-Name'),
                                               Button(0, 0, 50, 35, text='Lvl')], care_size=False)
        self.pokemon_info_text.set_rect(0, 0, 200, 35)
        self.pokemon_options = GuiContainer([Button(0, 0, 35, 35, text='+', image_normal=img, callback=self.add_pokemon),
                                             Button(0, 0, 35, 35, text='-', image_normal=img, callback=self.sub_pokemon)], care_size=False)
        self.pokemon_options.set_rect(0, 0, 100, 35)

        self.dialog_textfields = []
        self.dialog_cont = None
        self.gen_dialog_cont()
        self.pokemon_textfields = []
        self.pokemon_cont = None
        self.gen_pokemon_cont()
        self.rebuild_scene(self.last_width, self.last_height)

    def entry(self):
        self.clicked_npc(self.npc_editor.npc['i'])
        self.gen_dialog_cont()
        self.gen_pokemon_cont()

    def exit(self):
        pass

    def add_dialog(self):
        if self.npc_editor.npc is not None:
            if 'dialog' in self.npc_editor.npc:
                self.npc_editor.npc['dialog'].append('')
            else:
                self.npc_editor.npc['dialog'] = ['']
        self.gen_dialog_cont()
        self.rebuild_scene(self.last_width, self.last_height)

    def sub_dialog(self):
        if self.npc_editor.npc is not None and 'dialog' in self.npc_editor.npc:
            if len(self.npc_editor.npc['dialog']) > 0:
                del self.npc_editor.npc['dialog'][-1]
        self.gen_dialog_cont()
        self.rebuild_scene(self.last_width, self.last_height)

    def change_dialog(self, i):
        self.npc_editor.npc['dialog'][i] = self.dialog_textfields[i].text

    def gen_dialog_cont(self):
        self.dialog_textfields = []
        if self.npc_editor.npc is not None and 'dialog' in self.npc_editor.npc:
            dialog = self.npc_editor.npc['dialog']
            for i in range(len(dialog)):
                self.dialog_textfields.append(TextField(0, 0, 100, 35, text=dialog[i],
                                                        change=lambda x=i: self.change_dialog(x)))

        self.dialog_cont = GuiContainer(self.dialog_textfields + [self.dialog_options],
                                        with_columns=False, horizontal=False, care_size=False)

    def resize_dialog_textfields(self, w, h):
        for tf in self.dialog_textfields:
            tf.set_rect(0, 0, w, h)

    def add_pokemon(self):
        if self.npc_editor.npc is not None:
            if 'pokemon' in self.npc_editor.npc:
                self.npc_editor.npc['pokemon'].append({'name': '', 'lvl': ''})
            else:
                self.npc_editor.npc['pokemon'] = [{'name': '', 'lvl': ''}]
        self.gen_pokemon_cont()
        self.rebuild_scene(self.last_width, self.last_height)

    def sub_pokemon(self):
        if self.npc_editor.npc is not None and 'pokemon' in self.npc_editor.npc:
            if len(self.npc_editor.npc['pokemon']) > 0:
                del self.npc_editor.npc['pokemon'][-1]
        self.gen_pokemon_cont()
        self.rebuild_scene(self.last_width, self.last_height)

    def change_pokemon(self, i):
        self.npc_editor.npc['pokemon'][i]['name'] = self.pokemon_textfields[i].nodes[0].text
        self.npc_editor.npc['pokemon'][i]['lvl'] = self.pokemon_textfields[i].nodes[1].text

    def gen_pokemon_cont(self):
        self.pokemon_textfields = []
        if self.npc_editor.npc is not None and 'pokemon' in self.npc_editor.npc:
            pokemon = self.npc_editor.npc['pokemon']
            for i in range(len(pokemon)):
                g = GuiContainer([
                    TextField(0, 0, 100, 35, text=pokemon[i]['name'], change=lambda x=i: self.change_pokemon(x)),
                    TextField(0, 0, 40, 35, text=pokemon[i]['lvl'], change=lambda x=i: self.change_pokemon(x))
                ], care_size=False)
                g.set_rect(0, 0, 220, 35)
                self.pokemon_textfields.append(g)

        self.pokemon_cont = GuiContainer(self.pokemon_textfields + [self.pokemon_options],
                                         with_columns=False, horizontal=False, care_size=False)

    def rebuild_scene(self, width, height):
        self.last_width = width
        self.last_height = height
        self.bg.set_rect(0, 0, width, height)
        self.npc_cont.set_rect(120, 0, width, 100)
        self.resize_dialog_textfields(width - 250, 35)
        self.dialog_cont.set_rect(0, 150, width - 250, 200)
        self.pokemon_info_text.move(width - 220, 100)
        self.pokemon_cont.set_rect(width - 220, 150, width, 200)

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.rebuild_scene(event.w, event.h)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.npc_cont.handle_scroll(event):
                pass

        self.back_button.handle_event(event)
        self.save_button.handle_event(event)
        self.npc_cont.handle_event(event)
        self.dialog_cont.handle_event(event)
        self.pokemon_cont.handle_event(event)

    def render(self, screen):
        self.bg.draw(screen)
        self.back_button.draw(screen)
        self.save_button.draw(screen)
        self.npc_cont.draw(screen)
        self.dialog_cont.draw(screen)
        self.pokemon_cont.draw(screen)
        self.dialog_info_text.draw(screen)
        self.pokemon_info_text.draw(screen)
