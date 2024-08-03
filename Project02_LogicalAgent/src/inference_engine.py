from environment import Percept, Element
from knowledge_base import KnowledgeBase
from typing import List, Tuple, Dict, Set

# Define heuristic values
HEURISTIC_VALUES = {
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

    # Infer safe moves based on the current knowledge base with heuristics
    def infer_safe_moves(
        self,
        position: Tuple[int, int],
        grabbed_gold: Set[Tuple[int, int]],
        grabbed_HP: Set[Tuple[int, int]],
        visited: Set[Tuple[int, int]],
    ) -> List[Tuple[int, int]]:
        print("======== InferenceEngine: Infer Safe Moves =================")
        x, y = position
        directions = get_adjacent_cells(x, y, self.kb.grid_size)
        evaluated_moves = []

        # Check if current cell contains a healing potion
        if self.infer_healing_potion(position) and position not in grabbed_HP:
            evaluated_moves.append((position, HEURISTIC_VALUES[Element.HEALING_POTION]))
            print("Healing potion found at: ", position)

        # Check if current cell contains gold
        if self.infer_gold(position) and position not in grabbed_gold:
            evaluated_moves.append((position, HEURISTIC_VALUES[Element.GOLD]))
            print("Gold found at: ", position)

        for i, j in directions:
            if self.is_safe(i, j) and (i, j) not in visited:
                heuristic_value = self.evaluate_heuristic(i, j)
                evaluated_moves.append(((i, j), heuristic_value))

        # Sort moves by their heuristic value (descending)
        evaluated_moves.sort(key=lambda x: x[1], reverse=True)
        print("=================================================================")
        # Return the best move
        return [move for move, _ in evaluated_moves]

    # Check if a cell is safe
    def is_safe(self, x: int, y: int) -> bool:
        is_pit = self.kb.query(self.kb.encode(Element.PIT, x, y))
        is_wumpus = self.kb.query(self.kb.encode(Element.WUMPUS, x, y))
        if is_pit or is_wumpus:
            print(f"Cell ({x}, {y}) is not safe")
        return not is_pit and not is_wumpus

    # Evaluate the heuristic value of a given cell
    def evaluate_heuristic(self, x: int, y: int) -> int:
        """Evaluate the heuristic value of a given cell (x, y)."""
        total_value = 0

        # Consider elements that might be present at (x, y)
        for element, base_value in HEURISTIC_VALUES.items():
            # Check the likelihood of the element being present
            encoded_element = self.kb.encode(element, x, y)
            if self.kb.query(encoded_element):
                total_value += base_value

        return total_value

    # Infer the presence of a healing potion at a given position
    def infer_healing_potion(self, position: Tuple[int, int]) -> bool:
        x, y = position
        return self.kb.query(self.kb.encode(Element.HEALING_POTION, x, y))

    # Infer the presence of gold at a given position
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
                print(f"=============> Not {percept} at {position}")

    def infer_not_elements(self, position: Tuple[int, int], existing_element: Element):
        x, y = position
        if existing_element is None:
            existing_element = Element.AGENT
        for element in Element:
            if element == Element.AGENT or element == Element.SAFE:
                continue
            if element != existing_element:
                self.kb.add_clause([-self.kb.encode(element, x, y)])
                print(f"=============> Not {element} at {position}")

    def add_element(self, position: Tuple[int, int], element: Element):
        if element is not None:
            x, y = position
            self.kb.add_clause([self.kb.encode(element, x, y)])
            print(f"=============> Add {element} at {position}")


# Helper function to get adjacent cells
def get_adjacent_cells(x: int, y: int, grid_size: int) -> List[Tuple[int, int]]:
    adjacent_cells = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    adjacent_cells = [
        (i, j) for i, j in adjacent_cells if 0 <= i < grid_size and 0 <= j < grid_size
    ]
    return adjacent_cells
