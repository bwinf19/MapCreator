import os

from map import Map


class MapManager:
    def __init__(self, main, folder, tm, om):
        self.tm = tm
        self.om = om
        self.maps = {'world': os.path.join(main, 'world.json')}
        for filename in os.listdir(folder):
            path = os.path.join(folder, filename, 'inner-world.json')
            if os.path.isfile(path):
                self.maps[filename] = path
        self.select_map('world')

    def save(self):
        self.current_map.save()

    def toggle_grid(self):
        self.current_map.toggle_grid()

    def select_map(self, name):
        self.selected_map = self.maps[name]
        self.current_map = Map(self.tm, self.om, self.selected_map)
