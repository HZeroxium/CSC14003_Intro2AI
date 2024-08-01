# agent.py

from knowledge_base import KnowledgeBase
from inference_engine import InferenceEngine
from typing import Tuple, List
from environment import Percept
from enum import Enum


class Action(Enum):
    FORWARD = "forward"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    SHOOT = "shoot"
    GRAB = "grab"


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class Agent:
    def __init__(
        self,
        initial_position: Tuple[int, int] = (0, 0),
        health: int = 100,
        grid_size: int = 4,
    ):
        self.knowledge_base = KnowledgeBase(grid_size=grid_size)
        self.inference_engine = InferenceEngine()
        self.position = initial_position
        self.health = health
        self.grid_size = grid_size
        self.score = 0
        self.game_over = False
        self.current_direction = Direction.UP

    # Main function to choose the next action
    def choose_action(self, percepts: List[Tuple[Percept, int, int]]) -> str:
        # Use inference to decide the next action
        self.knowledge_base.update(percepts)
        safe_moves = self.inference_engine.infer_safe_moves(self.position)
        return self.select_action(safe_moves)

    # Select an action based on the safe moves
    def select_action(
        self, safe_moves: List[Tuple[int, int]]
    ) -> List[Tuple[Action, int, int]]:
        # Select an action from safe moves
        if not safe_moves:
            self.game_over = True
            return "end"
        else:
            next_position = safe_moves[0]
            target_direction: Direction = get_target_direction(
                self.position, next_position
            )
            turn_actions: List[Action] = get_actions(
                self.current_direction, target_direction
            )
            self.current_direction = target_direction
            actions: List[Tuple[Action, int, int]] = []
            # Perform the turn left, turn right actions to align the direction
            actions.extend(
                [
                    (action, self.position[0], self.position[1])
                    for action in turn_actions
                ]
            )
            # Move forward
            actions.append((Action.FORWARD, self.position[0], self.position[1]))
            return actions

    # Update the knowledge base with the new percept
    def update_knowledge(self, percept):
        self.knowledge_base.update(percept)

    def log_action(self, action):
        # Log the action taken
        print(f"Action taken: {action}")

    def is_game_over(self):
        return self.game_over

    def get_score(self):
        return self.score

    def handle_forward(self, position: Tuple[int, int]):
        self.position = position

    def turn_left(self, direction: Direction) -> Direction:
        if direction == Direction.UP:
            return Direction.LEFT
        elif direction == Direction.DOWN:
            return Direction.RIGHT
        elif direction == Direction.LEFT:
            return Direction.DOWN
        elif direction == Direction.RIGHT:
            return Direction.UP

    def turn_right(self, direction: Direction) -> Direction:
        if direction == Direction.UP:
            return Direction.RIGHT
        elif direction == Direction.DOWN:
            return Direction.LEFT
        elif direction == Direction.LEFT:
            return Direction.UP
        elif direction == Direction.RIGHT:
            return Direction.DOWN

    def handle_shoot(self, position: Tuple[int, int]):
        # Check if there is a Wumpus in the (x, y) position
        pass

    def handle_grab(self, position: Tuple[int, int]):
        is_healing_potion = self.inference_engine.infer_healing_potion(position)
        if is_healing_potion:
            self.health += 25
        else:
            self.score -= 10

        is_gold = self.inference_engine.infer_gold(position)
        if is_gold:
            self.score += 5000


# Helper function to get list of actions based on the current direction and the target direction
def get_actions(
    current_direction: Direction, target_direction: Direction
) -> List[Action]:
    actions = []
    if current_direction == target_direction:
        actions.append(Action.FORWARD)
    else:
        if current_direction == Direction.UP:
            if target_direction == Direction.LEFT:
                actions.append(Action.TURN_LEFT)
            elif target_direction == Direction.RIGHT:
                actions.append(Action.TURN_RIGHT)
            elif target_direction == Direction.DOWN:
                actions.append(Action.TURN_LEFT)
                actions.append(Action.TURN_LEFT)
        elif current_direction == Direction.DOWN:
            if target_direction == Direction.LEFT:
                actions.append(Action.TURN_RIGHT)
            elif target_direction == Direction.RIGHT:
                actions.append(Action.TURN_LEFT)
            elif target_direction == Direction.UP:
                actions.append(Action.TURN_LEFT)
                actions.append(Action.TURN_LEFT)
        elif current_direction == Direction.LEFT:
            if target_direction == Direction.UP:
                actions.append(Action.TURN_RIGHT)
            elif target_direction == Direction.DOWN:
                actions.append(Action.TURN_LEFT)
            elif target_direction == Direction.RIGHT:
                actions.append(Action.TURN_LEFT)
                actions.append(Action.TURN_LEFT)
        elif current_direction == Direction.RIGHT:
            if target_direction == Direction.UP:
                actions.append(Action.TURN_LEFT)
            elif target_direction == Direction.DOWN:
                actions.append(Action.TURN_RIGHT)
            elif target_direction == Direction.LEFT:
                actions.append(Action.TURN_LEFT)
                actions.append(Action.TURN_LEFT)
        actions.append(Action.FORWARD)
    return actions


# Helper function to get target direction based on current position and target position
def get_target_direction(
    current_position: Tuple[int, int], target_position: Tuple[int, int]
) -> Direction:
    x1, y1 = current_position
    x2, y2 = target_position
    if x1 == x2:
        if y2 > y1:
            return Direction.RIGHT
        else:
            return Direction.LEFT
    elif y1 == y2:
        if x2 > x1:
            return Direction.DOWN
        else:
            return Direction.UP
