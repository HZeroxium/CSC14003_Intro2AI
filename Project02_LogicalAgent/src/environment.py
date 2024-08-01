# environment.py

from enum import Enum
from typing import List, Tuple, Set, Dict
import pygame  # type: ignore

# **Input**: the given map is represented by matrix, which is stored in the input file, for example, map1.txt. The input file format is described as follows:

# - The first line contains an integer N, which is the size of map.
# - N next lines with each line represents a string. If room empty, it is marked by hyphen character (-). If room has some things or signal such as Wumpus(W), Pit(P), Breeze(B), Stench(S), Agent(A), Gold(G). Between two adjacent rooms is separated by a dot (.)
# - Input only includes Wumpus(W), Pit(P), Agent(A), Gold(G), Poisonous Gas(PG), Healing Potion(H_P). You need to update information about **Stench(S), Breeze(B), Whiff(WF), Glow(GL)** on the map based on input data.
# - For example:

# ``` plaintext
# -.-.W.-.P.-.-.P_G.-.-
# -.-.-.-.-.-.-.-.-.-
# ```

# | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
# | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
# | - | S | W | B, S | P | B | W | P_G | WF | - |
# | - | - | S | - | B | - | - | W | - | - |

CELL_SIZE = 300

COLORS: Dict[str, Tuple[int, int, int]] = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
}

TEXT_COLOR = COLORS["BLACK"]
GRID_COLOR = COLORS["BLACK"]
BACKGROUND_COLOR = COLORS["WHITE"]


class Percept(Enum):
    BREEZE = "B"
    STENCH = "S"
    SCREAM = "SC"
    WHIFF = "WF"
    GLOW = "GL"


class Element(Enum):
    AGENT = "A"
    WUMPUS = "W"
    GOLD = "G"
    PIT = "P"
    POISONOUS_GAS = "PG"
    HEALING_POTION = "HP"
    SAFE = None


ELEMENT_TO_PERCEPT: Dict[Element, Percept] = {
    Element.WUMPUS: Percept.STENCH,
    Element.PIT: Percept.BREEZE,
    Element.GOLD: Percept.GLOW,
    Element.POISONOUS_GAS: Percept.WHIFF,
    Element.AGENT: None,
    Element.HEALING_POTION: None,
}

PERCEPT_TO_ELEMENT: Dict[Percept, Element] = {
    Percept.STENCH: Element.WUMPUS,
    Percept.BREEZE: Element.PIT,
    Percept.GLOW: Element.GOLD,
    Percept.WHIFF: Element.POISONOUS_GAS,
}


class Environment:
    def __init__(self, map_file: str):
        self.map: List[List[Set[Enum]]] = list()
        self.load_map(map_file)
        self.size = len(self.map)

    # Convert map cell (set of strings) to a string with ',' as separator except '-'
    def cell_to_string(self, cell: Set[Enum]) -> str:
        if cell:
            return ", ".join([str(e.value) for e in cell if e is not None])

    # Update the neighbors of a given position based on the percept
    def update_map_neighbors(self, position: Tuple[int, int], element: Element):
        x, y = position
        percept = ELEMENT_TO_PERCEPT[element]
        for i, j in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if 0 <= i < len(self.map) and 0 <= j < len(self.map):
                self.map[i][j].add(percept)

    def load_map(self, map_file):
        with open(map_file, "r") as file:
            # Read raw data from the file
            n = int(file.readline().strip())
            map_data = [line.strip().split(".") for line in file]
            # print(map_data)

            # Initialize the map
            self.map = [[set() for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    element = map_data[i][j]
                    if element != "-":
                        element = Element(element)
                        self.map[i][j].add(element)
                        self.update_map_neighbors((i, j), element)

    # Return percepts based on the current position
    def get_percept(self, position: Tuple[int, int]) -> List[Tuple[int, int, Percept]]:
        x, y = position
        percepts = []
        for percept in Percept:
            if percept in self.map[x][y]:
                percepts.append((x, y, percept))

        return percepts

    def update(self, agent, action):
        if action == "move":
            new_position = action[1]
            agent.update_position(new_position)
        elif action == "shoot":
            self.handle_shoot(agent.position)

    def handle_shoot(self, position):
        x, y = position
        # Handle the consequences of shooting (e.g., killing Wumpus)
        if "W" in self.map[x][y]:
            self.map[x][y] = self.map[x][y].replace("W", "")

    def draw_grid(self, screen):
        n = self.size
        font = pygame.font.SysFont(None, 54)
        for row in range(n):
            for col in range(n):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BACKGROUND_COLOR, rect)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)
                cell = self.map[row][col]
                str_value = self.cell_to_string(cell)
                text_surface = font.render(str_value, True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)


def main():
    env = Environment("../data/input/map1.txt")
    pygame.init()
    screen = pygame.display.set_mode((env.size * CELL_SIZE, env.size * CELL_SIZE))
    pygame.display.set_caption("Wumpus World")
    env.draw_grid(screen)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    main()
