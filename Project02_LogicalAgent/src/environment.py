# environment.py

from enum import Enum
from typing import List, Tuple, Set, Dict
import pygame  # type: ignore
from utilities import (
    Action,
    Direction,
    Element,
    Percept,
    ELEMENT_TO_PERCEPT,
    ActionHandler,
)

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


class Environment:
    def __init__(self, map_file: str):
        self.map: List[List[Set[Enum]]] = list()
        self.load_map(map_file)
        self.size = len(self.map)
        self.visited = [[False for _ in range(self.size)] for _ in range(self.size)]

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
    def get_percept(self, position: Tuple[int, int]) -> List[Tuple[Enum, int, int]]:
        x, y = position
        percepts: List[Tuple[int, int, Percept]] = []
        for percept in Percept:
            if percept in self.map[x][y]:
                percepts.append((percept, x, y))

        return percepts

    # Return the element at the given position
    def get_element(self, position: Tuple[int, int]) -> Tuple[Element, int, int]:
        element: Element = Element.AGENT
        if position is None:
            print("Error: Agent position is None")
            return element, -1, -1
        x, y = position
        for element_ in Element:
            if element_ in self.map[x][y] and element_ != Element.SAFE:
                element = element_
        return element, x, y

    # Return the size of the map
    def get_map_size(self):
        return self.size

    # Return the agent's position
    def get_agent_position(self):
        for i in range(self.size):
            for j in range(self.size):
                if Element.AGENT in self.map[i][j]:
                    return (i, j)

    # Update the environment based on the agent's actions
    def update(
        self, agent, actions: List[Tuple[Action, int, int]]
    ) -> Tuple[Percept, int, int]:
        new_percept: Percept = None
        for action, x, y in actions:
            if action == Action.TURN_LEFT:
                print("Turning left...")
                agent.turn_left()
            elif action == Action.TURN_RIGHT:
                agent.turn_right()
            if action == Action.FORWARD:
                agent.handle_forward()
                self.visited[x][y] = True
                if Element.PIT in self.map[x][y]:
                    agent.game_over = True
                    return
                if Element.WUMPUS in self.map[x][y]:
                    agent.game_over = True
                    return
                if Element.POISONOUS_GAS in self.map[x][y]:
                    agent.health -= 25
                    return

            elif action == Action.SHOOT:
                # Shoot the arrow from the agent's position to the given direction
                is_killed = self.handle_shoot((x, y), agent.current_direction)
                agent.handle_shoot(is_killed)
            elif action == Action.GRAB:
                print("Grabbing...")
                agent.handle_grab((x, y))
                self.handle_grab((x, y))
            elif action == Action.CLIMB:
                print("Climbing...")
                agent.handle_climb()
                return
        return new_percept

    # Handle agent's shooting action
    def handle_shoot(self, position: Tuple[int, int], direction: Direction) -> bool:
        # Handle the consequences of shooting (e.g., killing Wumpus)
        wumpus_position = ActionHandler.handle_forward(position, direction)
        x, y = wumpus_position
        if Element.WUMPUS in self.map[x][y]:
            self.map[x][y] = self.map[x][y].remove(Element.WUMPUS)
            return True
        return False

    # Handle agent's grabbing action
    def handle_grab(self, position: Tuple[int, int]) -> Element:
        x, y = position
        # Handle the consequences of grabbing (e.g., picking up gold)
        if Element.GOLD in self.map[x][y]:
            self.map[x][y].remove(Element.GOLD)
            print("Current cell: ", self.map[x][y])
            # Remove Percept.GLOW in adjacent cells
            for i, j in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if 0 <= i < len(self.map) and 0 <= j < len(self.map):
                    self.map[i][j].remove(Percept.GLOW)
            return Element.GOLD
        # Pick up the healing potion
        if Element.HEALING_POTION in self.map[x][y]:
            self.map[x][y].remove(Element.HEALING_POTION)
            return Element.HEALING_POTION
        return None

    # Draw the grid on the screen
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


# def main():
#     env = Environment("../data/input/map1.txt")
#     pygame.init()
#     screen = pygame.display.set_mode((env.size * CELL_SIZE, env.size * CELL_SIZE))
#     pygame.display.set_caption("Wumpus World")
#     env.draw_grid(screen)
#     pygame.display.flip()

#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False


# if __name__ == "__main__":
#     main()
