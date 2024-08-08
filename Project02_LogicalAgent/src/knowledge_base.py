from pysat.formula import CNF  # type: ignore
from pysat.solvers import Solver  # type: ignore
from typing import List, Tuple, Dict, Set
from utilities import Percept, Element, PERCEPT_TO_ELEMENT
from enum import Enum

ENCODE_MAPPING: Dict[Enum, int] = {
    Element.WUMPUS: 1,
    Element.PIT: 2,
    Element.GOLD: 3,
    Element.POISONOUS_GAS: 4,
    Element.AGENT: 5,
    Element.HEALING_POTION: 6,
    Percept.STENCH: 7,
    Percept.BREEZE: 8,
    Percept.GLOW: 9,
    Percept.WHIFF: 10,
    Element.SAFE: 11,
}

DECODE_MAPPING: Dict[int, Enum] = {v: k for k, v in ENCODE_MAPPING.items()}


class KnowledgeBase:
    def __init__(self, grid_size: int = 4):
        self.facts = (
            CNF()
        )  # Conjunctive Normal Form of the knowledge base (list of clauses)
        self.solver = Solver(name="glucose4")  # SAT solver
        self.grid_size = grid_size

    def initialize_knowledge_base(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                self.add_uniqueness_rule(x, y)

    def add_uniqueness_rule(self, x: int, y: int):
        elements = [
            Element.WUMPUS,
            Element.PIT,
            Element.GOLD,
            Element.POISONOUS_GAS,
            Element.HEALING_POTION,
        ]
        for i in range(len(elements)):
            for j in range(i + 1, len(elements)):
                self.add_clause(
                    [-self.encode(elements[i], x, y), -self.encode(elements[j], x, y)]
                )

    def add_clause(self, rule: List[int]):
        self.facts.append(rule)  # Add the rule to the knowledge base
        self.solver.add_clause(rule)  # Add the rule to the SAT solver

    def query(self, literal: int) -> bool:
        is_satisfiable = self.solver.solve(assumptions=[-literal])
        return not is_satisfiable

    def update(self, percepts: List[Tuple[Percept, int, int]]):
        # print("===================== Knowledge Base Update =====================")
        for percept, x, y in percepts:
            self.add_clause([self.encode(percept, x, y)])
        self.infer_new_knowledge(set())

    @staticmethod
    def encode(symbol: Enum, x: int, y: int) -> int:
        return ENCODE_MAPPING[symbol] * 100 + x * 10 + y

    @staticmethod
    def decode(encoded: int) -> Tuple[Enum, int, int]:
        is_negative = encoded < 0
        encoded = abs(encoded)
        symbol = DECODE_MAPPING[encoded // 100]
        x = (encoded % 100) // 10
        y = encoded % 10
        if is_negative:
            return symbol, -x, -y
        return symbol, x, y

    @staticmethod
    def decode_rule(rule: List[int]) -> List[Tuple[Enum, int, int]]:
        return [KnowledgeBase.decode(literal) for literal in rule]

    def infer_new_knowledge(self, dangerous_cells: Set[Tuple[Element, int, int]]):
        # print(
        #     "===================== KnowledgeBase: Inferring New Knowledge ====================="
        # )
        new_inferences = []
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                new_inferences.extend(self.infer_from_percept(Percept.BREEZE, x, y))
                new_inferences.extend(self.infer_from_percept(Percept.STENCH, x, y))
                new_inferences.extend(self.infer_from_percept(Percept.GLOW, x, y))
                new_inferences.extend(self.infer_from_percept(Percept.WHIFF, x, y))
        for inference in new_inferences:
            self.add_clause(inference)
            element, x, y = self.decode(inference[0])
            dangerous_cells.add((element, x, y))

    def infer_from_percept(self, percept: Percept, x: int, y: int) -> List[int]:
        percept_location_encoded = self.encode(percept, x, y)
        new_inferences = []
        if self.query(percept_location_encoded):
            adjacent_cells = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            adjacent_cells = [
                (i, j)
                for i, j in adjacent_cells
                if 0 <= i < self.grid_size and 0 <= j < self.grid_size
            ]
            element = PERCEPT_TO_ELEMENT[percept]
            possible_element_locations_encoded = [
                self.encode(element, i, j) for i, j in adjacent_cells
            ]
            rule = [-percept_location_encoded] + possible_element_locations_encoded
            # print("+ Adding rule: ", self.decode_rule(rule))
            self.add_clause(rule)
            for location_encoded in possible_element_locations_encoded:
                if self.query(location_encoded):
                    new_inferences.append([location_encoded])
                    print("+ Adding inference: ", self.decode_rule([location_encoded]))
        return new_inferences


def main():
    # Initialize the knowledge base with a grid size of 3
    knowledge_base = KnowledgeBase(grid_size=3)
    # Add a fact that there is a breeze at (0, 0)
    knowledge_base.add_clause([knowledge_base.encode(Percept.BREEZE, 0, 0)])
    # Infer new knowledge based on the existing facts
    knowledge_base.infer_new_knowledge()
    # Add a fact that there is no pit at (0, 1)
    knowledge_base.add_clause([-knowledge_base.encode(Element.PIT, 0, 1)])

    # Query the knowledge base to check if there is a pit at (1. 0) -> False
    if not knowledge_base.query(knowledge_base.encode(Element.PIT, 1, 0)):
        print("There is no pit at (1, 0)")
    else:
        print("There is a pit at (1, 0)")


if __name__ == "__main__":
    main()
