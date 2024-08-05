# agent.py

from knowledge_base import KnowledgeBase
from inference_engine import InferenceEngine
from typing import Tuple, List, Set, Dict
from utilities import (
    Action,
    Direction,
    Percept,
    Element,
    get_actions,
    get_target_direction,
    ActionHandler,
)

INITIAL_POSITION = (0, 0)  # Initial position of the agent


# Agent class to represent the agent in the Wumpus World
class Agent:
    def __init__(
        self,
        initial_position: Tuple[int, int] = (0, 0),
        health: int = 100,
        grid_size: int = 4,
    ):
        self.knowledge_base = KnowledgeBase(
            grid_size=grid_size
        )  # Initialize the knowledge base
        self.inference_engine = InferenceEngine(
            knowledge_base=self.knowledge_base
        )  # Initialize the inference engine
        self.position = initial_position  # Current position of the agent
        self.health = health  # Health of the agent
        self.grid_size = grid_size  # Size of the grid
        self.score = 0  # Score of the agent
        self.game_over = False  # Flag to indicate if the game is over
        self.game_won = False  # Flag to indicate if the game is won
        self.current_direction = Direction.NORTH  # Current direction of the agent
        self.current_percepts: Set[Percept] = set()  # Current percepts of the agent
        self.current_action: List[Tuple[Action, int, int]] = (
            []
        )  # Current action of the agent
        self.grabbed_gold: Set[Tuple[int, int]] = set()  # Set of grabbed gold
        self.grabbed_HP: Set[Tuple[int, int]] = set()  # Set of grabbed healing potions
        self.visited: Set[Tuple[int, int]] = set()  # Set of visited cells
        self.parent: Dict[Tuple[int, int], Tuple[int, int]] = (
            {}
        )  # Parent dictionary to store the parent of each cell
        self.healing_potions: int = 0  # Number of healing potions grabbed
        self.dangerous_cells: Set[Tuple[Element, int, int]] = (
            set()
        )  # Set of dangerous cells

    def get_data(self):
        # Return a string with relevant agent data for display
        return f"Position: {self.position}, Health: {self.health}, Score: {self.get_score()}"


    # Main function to choose the next action
    def choose_action(
        self,
        percepts: List[Tuple[Percept, int, int]],
        element: Tuple[Element, int, int],
    ) -> str:
        # Check if current position is visited (it means the agent is back to the parent node)
        if self.position not in self.visited:
            self.visited.add(self.position)
            self.current_percepts.clear()
            for percept, x, y in percepts:
                self.current_percepts.add(percept)

            self.inference_engine.add_element(self.position, element[0])
            self.inference_engine.infer_not_elements(self.position, element[0])
            self.inference_engine.infer_not_percepts(
                self.position, self.current_percepts
            )
            # Use inference to decide the next action
            self.knowledge_base.update(percepts)
        safe_moves = self._infer_safe_moves()
        return self._select_action(safe_moves)

    # Update the knowledge base with the new elements
    def update_knowledge(self, new_percept: Tuple[Percept, int, int]):
        self.knowledge_base.infer_new_knowledge()

    def is_game_over(self):
        return self.game_over

    def is_game_won(self):
        return self.game_won

    def get_score(self):
        return self.score

    def handle_forward(self):
        self.score -= 10
        self.position = ActionHandler.handle_forward(
            self.position, self.current_direction
        )

    def turn_left(self) -> Direction:
        self.score -= 10
        self.current_direction = ActionHandler.turn_left(self.current_direction)

    def turn_right(self) -> Direction:
        self.score -= 10
        self.current_direction = ActionHandler.turn_right(self.current_direction)

    def handle_shoot(self, is_killed: bool):
        self.score -= 100
        shoot_position = ActionHandler.handle_forward(
            self.position, self.current_direction
        )
        if is_killed:
            self.knowledge_base.add_clause(
                [
                    -self.knowledge_base.encode(
                        Element.WUMPUS, shoot_position[0], shoot_position[1]
                    )
                ]
            )

    def handle_grab(self, position: Tuple[int, int]):
        self.score -= 10
        if self._is_healing_potion(position):
            self.grabbed_HP.add(position)
            self.healing_potions += 1
        if self._is_gold(position):
            self.score += 5000
            self.grabbed_gold.add(position)

    def _is_healing_potion(self, position: Tuple[int, int]) -> bool:
        return (
            self.inference_engine.infer_healing_potion(position)
            and position not in self.grabbed_HP
        )

    def _is_gold(self, position: Tuple[int, int]) -> bool:
        return (
            self.inference_engine.infer_gold(position)
            and position not in self.grabbed_gold
        )

    def heal(self):
        self.score -= 10
        if self.healing_potions > 0:
            self.health = min(100, self.health + 25)
            self.healing_potions -= 1

    def handle_climb(self):
        self.score += 10
        if self.position == INITIAL_POSITION:
            self.game_won = True

    def get_percept_string(self) -> str:
        # Format: (Percept1, Percept2, ...)
        return ", ".join(percept.name for percept in self.current_percepts) or "None"

    def get_action_string(self) -> str:
        # Format: [Action1, Action2, ...]. Example: [TURN_LEFT, FORWARD, GRAB]
        return ", ".join(action.name for action, _, _ in self.current_action) or "None"

    def get_dangerous_cells_str(self) -> str:
        return ", ".join(
            f"({element.value}, {x}, {y})" for element, x, y in self.dangerous_cells
        )

    def _infer_safe_moves(self) -> List[Tuple[int, int]]:
        return self.inference_engine.infer_safe_moves(
            self.position,
            self.grabbed_gold,
            self.grabbed_HP,
            self.visited,
            self.dangerous_cells,
        )

    def _select_action(self, safe_moves: List[Tuple[int, int]]) -> str:
        self.current_action = []
        if not safe_moves:
            return self._handle_no_safe_moves()
        return self._handle_safe_moves(safe_moves)

    def _handle_no_safe_moves(self) -> str:
        if len(self.visited) == self.grid_size * self.grid_size:
            self.game_over = True
            return "end"
        next_position = self.parent[self.position]
        self._move_to_position(next_position, is_back=True)
        return self.current_action

    def _handle_safe_moves(self, safe_moves: List[Tuple[int, int]]) -> str:
        next_position = safe_moves[0]
        if next_position == self.position:
            next_position = safe_moves[1]
            self.current_action.append(
                (Action.GRAB, self.position[0], self.position[1])
            )
        self._move_to_position(next_position)
        if next_position == INITIAL_POSITION:
            self.current_action.append(
                (Action.CLIMB, INITIAL_POSITION[0], INITIAL_POSITION[1])
            )
        return self.current_action

    def _move_to_position(self, next_position: Tuple[int, int], is_back: bool = False):
        if not is_back:
            self.parent[next_position] = self.position
        target_direction = get_target_direction(self.position, next_position)
        turn_actions = get_actions(self.current_direction, target_direction)
        self.current_action.extend(
            [(action, self.position[0], self.position[1]) for action in turn_actions]
        )

    # Write action to log file with format
    # (1, 1): move forward
    # (1, 2): turn right
    # (1, 2): shoot
    # ...
    def log_actions(self):
        with open("actions.log", "a") as f:
            for action, x, y in self.current_action:
                f.write(f"({x}, {y}): {action.name}\n")
