from enum import Enum
from typing import List, Tuple, Set
from utilities import (
    Action,
    Direction,
    Element,
    Percept,
    ELEMENT_TO_PERCEPT,
    ActionHandler,
)


class Environment:
    def __init__(self, map_file: str):
        self.map: List[List[Set[Enum]]] = []
        self.load_map(map_file)
        self.size = len(self.map)
        self.visited = [[False for _ in range(self.size)] for _ in range(self.size)]

    def cell_to_string(self, cell: Set[Enum]) -> str:
        return ", ".join([str(e.value) for e in cell if e is not None]) if cell else ""

    def update_map_neighbors(self, position: Tuple[int, int], element: Element):
        x, y = position
        percept = ELEMENT_TO_PERCEPT[element]
        for i, j in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if 0 <= i < len(self.map) and 0 <= j < len(self.map):
                self.map[i][j].add(percept)

    def load_map(self, map_file):
        with open(map_file, "r") as file:
            n = int(file.readline().strip())
            map_data = [line.strip().split(".") for line in file]

            self.map = [[set() for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    element_str = map_data[i][j]
                    if element_str != "-":
                        element = Element(element_str)
                        self.map[i][j].add(element)
                        self.update_map_neighbors((i, j), element)

    def get_percept(self, position: Tuple[int, int]) -> List[Tuple[Enum, int, int]]:
        x, y = position
        return [(percept, x, y) for percept in Percept if percept in self.map[x][y]]

    def get_element(self, position: Tuple[int, int]) -> Tuple[Element, int, int]:
        if not position:
            print("Error: Agent position is None")
            return Element.AGENT, -1, -1
        x, y = position
        for element in Element:
            if element in self.map[x][y] and element != Element.SAFE:
                return element, x, y
        return Element.AGENT, x, y

    def get_map_size(self):
        return self.size

    def get_agent_position(self):
        for i in range(self.size):
            for j in range(self.size):
                if Element.AGENT in self.map[i][j]:
                    return (i, j)

    def update(
        self, agent, actions: List[Tuple[Action, int, int]]
    ) -> Tuple[Percept, int, int]:
        for action, x, y in actions:
            if action == Action.TURN_LEFT:
                agent.turn_left()
            elif action == Action.TURN_RIGHT:
                agent.turn_right()
            elif action == Action.FORWARD:
                agent.handle_forward()
                self.visited[x][y] = True
                if Element.PIT in self.map[x][y] or Element.WUMPUS in self.map[x][y]:
                    agent.game_over = True
                    return
                if Element.POISONOUS_GAS in self.map[x][y]:
                    agent.health -= 25
                    return
            elif action == Action.SHOOT:
                is_killed = self.handle_shoot((x, y), agent.current_direction)
                agent.handle_shoot(is_killed)
            elif action == Action.GRAB:
                agent.handle_grab((x, y))
                self.handle_grab((x, y))
            elif action == Action.CLIMB:
                agent.handle_climb()
                return
        return None

    def handle_shoot(self, position: Tuple[int, int], direction: Direction) -> bool:
        wumpus_position = ActionHandler.handle_forward(position, direction)
        x, y = wumpus_position
        if Element.WUMPUS in self.map[x][y]:
            self.map[x][y].remove(Element.WUMPUS)
            return True
        return False

    def handle_grab(self, position: Tuple[int, int]) -> Element:
        x, y = position
        if Element.GOLD in self.map[x][y]:
            self.map[x][y].remove(Element.GOLD)
            for i, j in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if 0 <= i < len(self.map) and 0 <= j < len(self.map):
                    self.map[i][j].discard(Percept.GLOW)
            return Element.GOLD
        if Element.HEALING_POTION in self.map[x][y]:
            self.map[x][y].remove(Element.HEALING_POTION)
            return Element.HEALING_POTION
        return None


# Uncomment the following lines to enable running the script as a standalone application
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
