# program.py


class Program:
    def __init__(self, map_file):
        self.map = self.load_map(map_file)

    def load_map(self, map_file):
        # Load the map from file
        with open(map_file, "r") as file:
            size = int(file.readline().strip())
            map_data = [line.strip().split(".") for line in file]
        return map_data

    def get_percept(self, position):
        # Return percepts based on the current position
        x, y = position
        percept = self.map[x][y]
        return percept

    def update_map(self, position, new_info):
        x, y = position
        self.map[x][y] = new_info
