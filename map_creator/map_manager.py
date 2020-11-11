import os

from map import Map


class MapManager:
    def __init__(self, main, folder, tm, om, trm, gm):
        self.tm = tm
        self.om = om
        self.trm = trm
        self.gm = gm
        self.maps = {'world': os.path.join(main, 'world.json')}
        for filename in os.listdir(folder):
            path = os.path.join(folder, filename, 'inner-world.json')
            if os.path.isfile(path):
                self.maps[filename] = path
        self.current_map = None
        self.select_map('world')

    def save(self):
        if self.current_map is not None:
            self.current_map.save()

    def toggle_grid(self):
        self.current_map.toggle_grid()

    def select_map(self, name):
        self.save()
        selected_map = self.maps[name]
        self.current_map = Map(self.tm, self.om, self.trm, self, selected_map)
