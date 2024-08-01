# knowledge_base.py
from pysat.formula import CNF  # type: ignore
from pysat.solvers import Solver  # type: ignore
from typing import List, Tuple, Dict
from enum import Enum
from environment import Percept, Element


class KnowledgeBase:
    def __init__(self):
        self.facts = (
            CNF()
        )  # Conjunctive Normal Form of the knowledge base (list of clauses)
        self.solver = Solver(name="glucose4")  # SAT solver
        self.add_rules()  # Add initial rules to the knowledge base

    def add_fact(self, fact: List[int]):
        self.facts.append(
            fact
        )  # Add the fact to the knowledge base. Example: [B(x, y)]
        self.solver.add_clause(
            fact
        )  # Add the fact to the SAT solver. Example: [B(x, y)]

    def add_rule(self, rule: List[int]):
        self.facts.append(
            rule
        )  # Add the rule to the knowledge base. Example: [B(x, y) | B(x+1, y)]
        self.solver.add_clause(
            rule
        )  # Add the rule to the SAT solver. Example: [B(x, y) | B(x+1, y)]

    def add_rules(self):
        pass

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
        mapping: Dict[Enum, int] = {
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
        hash_value = mapping[symbol] * 100 + x * 10 + y
        # Check if the hash value is overflown
        if hash_value < 0:
            return -hash_value
        return hash_value

    def infer_new_knowledge(self):
        new_inferences = []
        # For simplicity, assuming a 4x4 grid. This can be adjusted as needed.
        grid_size = 3

        # Iterate over all possible cells in the grid
        for x in range(grid_size):
            for y in range(grid_size):
                # Check for Breezes and infer about Pits
                print("=====================================")
                adjacent_cells = [
                    (x + 1, y),
                    (x - 1, y),
                    (x, y + 1),
                    (x, y - 1),
                ]

                # Remove unreachable cells

                adjacent_cells = [
                    (i, j)
                    for i, j in adjacent_cells
                    if i >= 0 and i < grid_size and j >= 0 and j < grid_size
                ]

                if self.query(self.encode(Percept.BREEZE, x, y)):
                    # Breeze(x,y) <=> Pit(x+1,y) | Pit(x-1,y) | Pit(x,y+1) | Pit(x,y-1)
                    # B <=> P1 | P2 | P3 | P4
                    # Convert to CNF:
                    # (!B | P1 | P2 | P3 | P4) & (B | !P1) & (B | !P2) & (B | !P3) & (B | !P4)
                    possible_pit_locations = [
                        self.encode(Element.PIT, i, j) for i, j in adjacent_cells
                    ]

                    # Add rule to knowledge base
                    # Add (!B | P1 | P2 | P3 | P4)
                    rule = [-self.encode(Percept.BREEZE, x, y)] + possible_pit_locations
                    print("Adding rule: ", rule)
                    self.add_rule(rule)
                    # Add (B | !P1) & (B | !P2) & (B | !P3) & (B | !P4)
                    for pit in possible_pit_locations:
                        rule = [self.encode(Percept.BREEZE, x, y), -pit]
                        print("Adding rule: ", rule)
                        self.add_rule(rule)

                    print("With breeze at: ", x, y)
                    print("Possible pit locations: ", possible_pit_locations)
                    for pit in possible_pit_locations:
                        if self.query(pit):  # If it's not proven false
                            print("Adding pit: ", pit)
                            new_inferences.append(
                                [pit]
                            )  # Add the inferred pit to new inferences

                # if not self.query(self.encode(Percept.BREEZE, x, y)):
                #     possible_safe_locations = [
                #         self.encode(Element.SAFE, i, j) for i, j in adjacent_cells
                #     ]
                #     print("Without breeze at: ", x, y)
                #     print("Possible safe locations: ", possible_safe_locations)
                #     for safe in possible_safe_locations:
                #         if not self.query(safe):
                #             pass
                # # Check for Stenches and infer about Wumpus
                # if self.query(self.encode(Percept.STENCH, x, y)):
                #     possible_wumpus_locations = [
                #         self.encode(Element.WUMPUS, x + 1, y),
                #         self.encode(Element.WUMPUS, x - 1, y),
                #         self.encode(Element.WUMPUS, x, y + 1),
                #         self.encode(Element.WUMPUS, x, y - 1),
                #     ]
                #     for wumpus in possible_wumpus_locations:
                #         if not self.query(wumpus):  # If it's not proven false
                #             new_inferences.append([wumpus])

                # # Check for Glows and infer about Gold
                # if self.query(self.encode(Percept.GLOW, x, y)):
                #     possible_gold_locations = [
                #         self.encode(Element.GOLD, x + 1, y),
                #         self.encode(Element.GOLD, x - 1, y),
                #         self.encode(Element.GOLD, x, y + 1),
                #         self.encode(Element.GOLD, x, y - 1),
                #     ]
                #     for gold in possible_gold_locations:
                #         if not self.query(gold):  # If it's not proven false
                #             new_inferences.append([gold])

                # # Check for Whiffs and infer about Poisonous Gas
                # if self.query(self.encode(Percept.WHIFF, x, y)):
                #     possible_pg_locations = [
                #         self.encode(Element.POISONOUS_GAS, x + 1, y),
                #         self.encode(Element.POISONOUS_GAS, x - 1, y),
                #         self.encode(Element.POISONOUS_GAS, x, y + 1),
                #         self.encode(Element.POISONOUS_GAS, x, y - 1),
                #     ]
                #     for pg in possible_pg_locations:
                #         if not self.query(pg):  # If it's not proven false
                #             new_inferences.append([pg])

        # Add new inferences to the knowledge base
        for inference in new_inferences:
            self.add_fact(inference)


def main():
    knowledge_base = KnowledgeBase()
    # Create a simple knowledge base that can infer about there being a pit in (0, 0)

    # .P.B.-.-
    # .B.-.-.-
    # .-.-.-.-
    # .-.-.-.-

    # if knowledge_base.query(knowledge_base.encode(Percept.BREEZE, 0, 0)):
    #     print("Breeze at (0, 0) is consistent with the knowledge base.")

    # knowledge_base.add_fact([knowledge_base.encode(Percept.BREEZE, 0, 0)])
    # if knowledge_base.query(knowledge_base.encode(Percept.BREEZE, 0, 0)):
    #     print("Breeze at (0, 0) is consistent with the knowledge base.")

    # knowledge_base.infer_new_knowledge()

    # if knowledge_base.query(knowledge_base.encode(Percept.BREEZE, 0, 0)):
    #     print("Breeze at (0, 0) is consistent with the knowledge base.")

    # With 2x2 grid, if there is a breeze at (1, 0) and (0, 1), and (1, 1) is safe, then there is a pit at (0, 0)
    knowledge_base.add_fact([knowledge_base.encode(Percept.BREEZE, 0, 1)])
    knowledge_base.add_fact([knowledge_base.encode(Percept.BREEZE, 1, 0)])
    knowledge_base.add_fact([-knowledge_base.encode(Element.PIT, 1, 1)])
    knowledge_base.infer_new_knowledge()

    if knowledge_base.query(knowledge_base.encode(Element.PIT, 0, 0)):
        print("Pit at (0, 0) is consistent with the knowledge base.")
    # if knowledge_base.query(knowledge_base.encode(Percept.BREEZE, 0, 1)):
    #     print("Breeze at (0, 1) is consistent with the knowledge base.")

    # if knowledge_base.query(knowledge_base.encode(Percept.BREEZE, 1, 0)):
    #     print("Breeze at (1, 0) is consistent with the knowledge base.")
    # knowledge_base.infer_new_knowledge()

    # knowledge_base.add_fact([knowledge_base.encode(Percept.BREEZE, 1, 0)])
    # knowledge_base.infer_new_knowledge()


if __name__ == "__main__":
    main()
