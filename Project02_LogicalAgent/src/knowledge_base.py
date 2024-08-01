# knowledge_base.py
from pysat.formula import CNF  # type: ignore
from pysat.solvers import Solver  # type: ignore
from typing import List, Tuple, Dict
from enum import Enum
from environment import Percept, Element, PERCEPT_TO_ELEMENT

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
}

DECODE_MAPPING: Dict[int, Enum] = {v: k for k, v in ENCODE_MAPPING.items()}


class KnowledgeBase:
    def __init__(self, grid_size: int = 4):
        self.facts = (
            CNF()
        )  # Conjunctive Normal Form of the knowledge base (list of clauses)
        self.solver = Solver(name="glucose4")  # SAT solver
        self.grid_size = grid_size

    def add_clause(self, rule: List[int]):
        self.facts.append(
            rule
        )  # Add the rule to the knowledge base. Example: [B(x, y) | B(x+1, y)]
        self.solver.add_clause(
            rule
        )  # Add the rule to the SAT solver. Example: [B(x, y) | B(x+1, y)]

    # Check if a literal is consistent with the knowledge base (i.e., not proven false)
    def query(self, literal: int) -> bool:
        print("Querying: ", literal)
        # Temporary addition of the negation of the literal to check consistency
        is_satisfiable = self.solver.solve(assumptions=[-literal])
        return not is_satisfiable

    def update(self, percepts: List[Tuple[Percept, int, int]]):
        # Process percepts and update knowledge base
        for percept, x, y in percepts:
            # Example: Adding the fact 'B(x, y)' if a breeze is perceived
            if percept == Percept.BREEZE:
                self.add_fact([self.encode(percept, x, y)])
            if percept == Percept.STENCH:
                self.add_fact([self.encode(percept, x, y)])
            if percept == Percept.GLOW:
                self.add_fact([self.encode(percept, x, y)])
            if percept == Percept.WHIFF:
                self.add_fact([self.encode(percept, x, y)])
            # Add more percepts as needed
        self.infer_new_knowledge()

    @staticmethod
    def encode(symbol: Enum, x: int, y: int) -> int:
        # Encode a logical variable uniquely
        hash_value = ENCODE_MAPPING[symbol] * 100 + x * 10 + y
        return hash_value

    @staticmethod
    def decode(encoded: int) -> Tuple[Enum, int, int]:
        # Decode a logical variable
        symbol = DECODE_MAPPING[encoded // 100]
        x = (encoded % 100) // 10
        y = encoded % 10
        return symbol, x, y

    def infer_new_knowledge(self):
        new_inferences = []
        # For simplicity, assuming a 4x4 grid. This can be adjusted as needed.
        grid_size = 2

        # Iterate over all possible cells in the grid
        for x in range(grid_size):
            for y in range(grid_size):
                # Infer new knowledge based on the percept
                new_inferences.extend(
                    self.infer_from_percept(Percept.BREEZE, x, y, grid_size)
                )
                new_inferences.extend(
                    self.infer_from_percept(Percept.STENCH, x, y, grid_size)
                )
                new_inferences.extend(
                    self.infer_from_percept(Percept.GLOW, x, y, grid_size)
                )
                new_inferences.extend(
                    self.infer_from_percept(Percept.WHIFF, x, y, grid_size)
                )
                # Add more percepts as needed

        # Add new inferences to the knowledge base
        for inference in new_inferences:
            self.add_clause(inference)

    # Helper function to infer from percept
    def infer_from_percept(self, percept: Percept, x: int, y: int, grid_size: int):
        # Infer new knowledge based on the percept
        # Denote: Percept = P, Element = E
        # Rule: P(x,y) <=> E(x+1,y) | E(x-1,y) | E(x,y+1) | E(x,y-1)
        # Convert to CNF:
        # (!P | E1 | E2 | E3 | E4) & (P | !E1) & (P | !E2) & (P | !E3) & (P | !E4)

        percept_location_encoded = self.encode(percept, x, y)
        new_inferences = []
        if self.query(percept_location_encoded):
            adjacent_cells = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            adjacent_cells = [
                (i, j)
                for i, j in adjacent_cells
                if 0 <= i < grid_size and 0 <= j < grid_size
            ]

            element = PERCEPT_TO_ELEMENT[percept]

            percept_location_encoded = self.encode(percept, x, y)
            possible_element_locations_encoded = [
                self.encode(element, i, j) for i, j in adjacent_cells
            ]

            # Add rule (!P | E1 | E2 | E3 | E4) to the knowledge base
            rule = [-percept_location_encoded] + possible_element_locations_encoded
            print("+ Adding rule: ", rule)
            self.add_clause(rule)

            # Add rules (P | !E1) & (P | !E2) & (P | !E3) & (P | !E4) to the knowledge base
            for element_location_encoded in possible_element_locations_encoded:
                rule = [percept_location_encoded, -element_location_encoded]
                self.add_clause(rule)
                if self.query(element_location_encoded):
                    new_inferences.append([element_location_encoded])
                    print("====> Inferred: ", element_location_encoded)

        return new_inferences


def main():
    knowledge_base = KnowledgeBase()

    # With 2x2 grid, if there is a breeze at (1, 0) and (0, 1), and (1, 1) is safe, then there is a pit at (0, 0)
    knowledge_base.add_clause([knowledge_base.encode(Percept.BREEZE, 0, 1)])
    knowledge_base.add_clause([knowledge_base.encode(Percept.BREEZE, 1, 0)])
    knowledge_base.add_clause([-knowledge_base.encode(Element.PIT, 1, 1)])
    knowledge_base.infer_new_knowledge()

    if knowledge_base.query(knowledge_base.encode(Element.PIT, 0, 0)):
        print("Pit at (0, 0) is consistent with the knowledge base.")


if __name__ == "__main__":
    main()
