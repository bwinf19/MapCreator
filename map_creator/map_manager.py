import os

from map import Map


class MapManager:
    def __init__(self, main, folder, tm, om, trm, gm):
        self.tm = tm
        self.om = om
        self.trm = trm
        self.gm = gm
        self.main = main
        self.folder = folder
        self.maps = {}
        self.refresh()
        self.current_map = None
        self.current_name = None
        self.select_map('world')

    def refresh(self):
        self.maps = {'world': os.path.join(self.main, 'world.json')}
        for filename in os.listdir(self.folder):
            path = os.path.join(self.folder, filename, 'inner-world.json')
            if os.path.isfile(path):
                self.maps[filename] = path

    def save(self):
        if self.current_map is not None:
            self.current_map.save()

    def set_current_map(self):
        selected_map = self.maps[self.current_name]
        self.current_map = Map(self.tm, self.om, self.trm, self, selected_map)

    def select_map(self, name):
        self.save()
        self.current_name = name
        self.set_current_map()
