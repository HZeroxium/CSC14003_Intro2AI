from environment import Percept, Element
from knowledge_base import KnowledgeBase
from typing import List, Tuple, Dict

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
    def infer_safe_moves(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        print("=== Infer Safe Moves ===")
        x, y = position
        directions = get_adjacent_cells(x, y, self.kb.grid_size)
        evaluated_moves = []

        for i, j in directions:
            if self.is_safe(i, j):
                heuristic_value = self.evaluate_heuristic(i, j)
                evaluated_moves.append(((i, j), heuristic_value))

        # Sort moves by their heuristic value (descending)
        evaluated_moves.sort(key=lambda x: x[1], reverse=True)
        # Return the best move
        return [move for move, _ in evaluated_moves]

    def is_safe(self, x: int, y: int) -> bool:
        is_pit = self.kb.query(self.kb.encode(Element.PIT, x, y))
        is_wumpus = self.kb.query(self.kb.encode(Element.WUMPUS, x, y))
        return not is_pit and not is_wumpus

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

    def infer_healing_potion(self, position: Tuple[int, int]) -> bool:
        x, y = position
        return self.kb.query(self.kb.encode(Element.HEALING_POTION, x, y))

    def infer_gold(self, position: Tuple[int, int]) -> bool:
        x, y = position
        return self.kb.query(self.kb.encode(Element.GOLD, x, y))


# Helper function to get adjacent cells
def get_adjacent_cells(x: int, y: int, grid_size: int) -> List[Tuple[int, int]]:
    adjacent_cells = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    adjacent_cells = [
        (i, j) for i, j in adjacent_cells if 0 <= i < grid_size and 0 <= j < grid_size
    ]
    return adjacent_cells
