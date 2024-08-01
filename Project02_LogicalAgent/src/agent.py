# agent.py

from knowledge_base import KnowledgeBase
from inference_engine import InferenceEngine
from typing import Tuple, List
from environment import Percept


class Agent:
    def __init__(
        self,
        initial_position: Tuple[int, int] = (0, 0),
        health: int = 100,
    ):
        self.knowledge_base = KnowledgeBase()
        self.inference_engine = InferenceEngine()
        self.position = initial_position
        self.health = health
        self.score = 0
        self.game_over = False

    def choose_action(self, percepts: List[Tuple[int, int, Percept]]):
        # Use inference to decide the next action
        self.knowledge_base.update(percepts)
        safe_moves = self.inference_engine.infer_safe_moves(self.position)
        return self.select_action(safe_moves)

    def select_action(self, safe_moves):
        # Select an action from safe moves
        if not safe_moves:
            self.game_over = True
            return "end"
        # Example: prioritizing moves
        return safe_moves[0]

    def update_knowledge(self, percept):
        self.knowledge_base.update(percept)

    def log_action(self, action):
        # Log the action taken
        print(f"Action taken: {action}")

    def is_game_over(self):
        return self.game_over

    def get_score(self):
        return self.score
