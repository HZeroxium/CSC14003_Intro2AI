# inference_engine.py

from environment import Percept, Element
from knowledge_base import KnowledgeBase
from typing import List, Tuple


class InferenceEngine:
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base

    def infer_safe_moves(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = position
        moves = []
        directions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for i, j in directions:
            if self.is_safe(i, j):
                moves.append((i, j))
        return moves

    def is_safe(self, x: int, y: int) -> bool:
        return (
            self.kb.query(-self.kb.encode(Element.PIT.value, x, y))
            and self.kb.query(-self.kb.encode(Element.WUMPUS.value, x, y))
            and self.kb.query(-self.kb.encode(Element.POISONOUS_GAS.value, x, y))
        )
