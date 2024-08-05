from environment import Percept, Element
from knowledge_base import KnowledgeBase
from typing import List, Tuple, Set, Dict

# Define heuristic values
HEURISTIC_VALUES: Dict[Element, int] = {
    Element.WUMPUS: -100,
    Element.PIT: -200,
    Element.GOLD: 100,
    Element.POISONOUS_GAS: -150,
    Element.AGENT: 0,
    Element.HEALING_POTION: 50,
    Percept.STENCH: -10,
    Percept.BREEZE: -10,
    Percept.GLOW: 50,
    Percept.WHIFF: -20,
}


class InferenceEngine:
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base

    def infer_safe_moves(
        self,
        position: Tuple[int, int],
        grabbed_gold: Set[Tuple[int, int]],
        grabbed_HP: Set[Tuple[int, int]],
        visited: Set[Tuple[int, int]],
        dangerous_cells: Set[Tuple[Element, int, int]],
    ) -> List[Tuple[int, int]]:
        # print("======== InferenceEngine: Infer Safe Moves =================")
        x, y = position
        directions = get_adjacent_cells(x, y, self.kb.grid_size)
        evaluated_moves = []

        if self.infer_healing_potion(position) and position not in grabbed_HP:
            evaluated_moves.append((position, HEURISTIC_VALUES[Element.HEALING_POTION]))
            print("Healing potion found at: ", position)

        if self.infer_gold(position) and position not in grabbed_gold:
            evaluated_moves.append((position, HEURISTIC_VALUES[Element.GOLD]))
            print("Gold found at: ", position)

        for i, j in directions:
            if self.is_safe(i, j) and (i, j) not in visited:
                heuristic_value = self.evaluate_heuristic(i, j)
                evaluated_moves.append(((i, j), heuristic_value))
            if not self.is_safe(i, j):
                self.add_dangerous_cell(i, j, dangerous_cells)

        evaluated_moves.sort(key=lambda x: x[1], reverse=True)
        # print("=================================================================")
        # print("Safe moves: ", [move for move, _ in evaluated_moves])

        if not evaluated_moves:
            not_visited_cells = self.get_not_visited_cells(visited)
            not_safe_cells = self.get_not_safe_cells(visited)
            if not_visited_cells == not_safe_cells and (0, 0) in get_adjacent_cells(
                x, y, self.kb.grid_size
            ):
                return [(0, 0)]

        return [move for move, _ in evaluated_moves]

    def add_dangerous_cell(
        self, x: int, y: int, dangerous_cells: Set[Tuple[Element, int, int]]
    ):
        if self.kb.query(self.kb.encode(Element.WUMPUS, x, y)):
            dangerous_cells.add((Element.WUMPUS, x, y))
            self.infer_not_elements((x, y), Element.WUMPUS)
        if self.kb.query(self.kb.encode(Element.PIT, x, y)):
            dangerous_cells.add((Element.PIT, x, y))
            self.infer_not_elements((x, y), Element.PIT)
        if self.kb.query(self.kb.encode(Element.POISONOUS_GAS, x, y)):
            dangerous_cells.add((Element.POISONOUS_GAS, x, y))
            self.infer_not_elements((x, y), Element.POISONOUS_GAS)

    def is_safe(self, x: int, y: int) -> bool:
        is_pit = self.kb.query(self.kb.encode(Element.PIT, x, y))
        is_wumpus = self.kb.query(self.kb.encode(Element.WUMPUS, x, y))
        is_poisonous_gas = self.kb.query(self.kb.encode(Element.POISONOUS_GAS, x, y))

        # if is_pit:
        #     print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Pit at {x, y}")
        # if is_wumpus:
        #     print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Wumpus at {x, y}")
        # if is_poisonous_gas:
        #     print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Poisonous gas at {x, y}")

        return not is_pit and not is_wumpus and not is_poisonous_gas

    def evaluate_heuristic(self, x: int, y: int) -> int:
        total_value = 0
        for element, base_value in HEURISTIC_VALUES.items():
            encoded_element = self.kb.encode(element, x, y)
            if self.kb.query(encoded_element):
                total_value += base_value
        return total_value

    def infer_healing_potion(self, position: Tuple[int, int]) -> bool:
        x, y = position
        return self.kb.query(self.kb.encode(Element.HEALING_POTION, x, y))

    def infer_gold(self, position: Tuple[int, int]) -> bool:
        x, y = position
        return self.kb.query(self.kb.encode(Element.GOLD, x, y))

    def infer_not_percepts(
        self, position: Tuple[int, int], existing_percepts: Set[Percept]
    ):
        x, y = position
        for percept in Percept:
            if percept not in existing_percepts:
                self.kb.add_clause([-self.kb.encode(percept, x, y)])
                # print(f"=============> Not {percept} at {position}")

    def infer_not_elements(self, position: Tuple[int, int], existing_element: Element):
        x, y = position
        for element in Element:
            if element != existing_element and element != Element.SAFE:
                self.kb.add_clause([-self.kb.encode(element, x, y)])
                # print(f"=============> Not {element} at {position}")

    def add_element(self, position: Tuple[int, int], element: Element):
        if element is not Element.AGENT:
            x, y = position
            self.kb.add_clause([self.kb.encode(element, x, y)])
            # print(f"=============> Add {element} at {position}")

    def get_not_visited_cells(
        self, visited: Set[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        return [
            (i, j)
            for i in range(self.kb.grid_size)
            for j in range(self.kb.grid_size)
            if (i, j) not in visited
        ]

    def get_not_safe_cells(
        self, visited: Set[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        return [
            (i, j)
            for i in range(self.kb.grid_size)
            for j in range(self.kb.grid_size)
            if not self.is_safe(i, j) and (i, j) not in visited
        ]


# Helper function to get adjacent cells
def get_adjacent_cells(x: int, y: int, grid_size: int) -> List[Tuple[int, int]]:
    adjacent_cells = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return [
        (i, j) for i, j in adjacent_cells if 0 <= i < grid_size and 0 <= j < grid_size
    ]
