# knowledge_base.py

from pysat.solvers import Solver  # type: ignore


class KnowledgeBase:
    def __init__(self):
        self.facts = set()  # Stores known facts
        self.rules = []  # Stores logical rules

    def add_fact(self, fact):
        self.facts.add(fact)

    def add_rule(self, rule):
        self.rules.append(rule)

    def query(self, query):
        solver = Solver()
        for rule in self.rules:
            solver.add_clause(rule)
        return solver.solve([query])

    def update(self, percepts):
        # Update facts based on percepts
        for percept in percepts:
            self.add_fact(percept)
        self.infer_new_knowledge()

    def infer_new_knowledge(self):
        # Infer new facts using rules and current facts
        new_facts = set()
        for rule in self.rules:
            if self.apply_rule(rule):
                new_facts.add(rule.consequent)
        self.facts.update(new_facts)

    def apply_rule(self, rule):
        # Check if a rule can be applied based on current facts
        return all(fact in self.facts for fact in rule.antecedents)
