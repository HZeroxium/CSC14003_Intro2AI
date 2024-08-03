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

actionHandler = ActionHandler()


class Agent:
    def __init__(
        self,
        initial_position: Tuple[int, int] = (0, 0),
        health: int = 100,
        grid_size: int = 4,
    ):
        self.knowledge_base = KnowledgeBase(grid_size=grid_size)
        self.inference_engine = InferenceEngine(knowledge_base=self.knowledge_base)
        self.position = initial_position
        self.health = health
        self.grid_size = grid_size
        self.score = 0
        self.game_over = False
        self.current_direction = Direction.NORTH
        self.current_percepts: Set[Percept] = set()
        self.current_action: List[Tuple[Action, int, int]] = []
        self.grabbed_gold: Set[Tuple[int, int]] = set()
        self.grabbed_HP: Set[Tuple[int, int]] = set()
        self.visited: Set[Tuple[int, int]] = set()
        self.parent: Dict[Tuple[int, int], Tuple[int, int]] = {}
        self.healing_potions: int = 0

    # Main function to choose the next action
    def choose_action(
        self,
        percepts: List[Tuple[Percept, int, int]],
        element: Tuple[Element, int, int],
    ) -> str:
        # Update the current percepts
        self.visited.add(self.position)
        self.current_percepts.clear()
        for percept, x, y in percepts:
            self.current_percepts.add(percept)
        print("============= Agent: Choose Action =================")
        # print("=============> Current percepts: ", self.current_percepts)
        print("=============> Current elements: ", element)
        # Update the knowledge base with the new elements if elements is not None
        self.inference_engine.add_element(self.position, element[0])

        # Infer that there is no element except the current element at the current position
        self.inference_engine.infer_not_elements(self.position, element[0])
        # Get percepts that not exists in percepts
        self.inference_engine.infer_not_percepts(self.position, self.current_percepts)
        # Use inference to decide the next action
        self.knowledge_base.update(percepts)
        safe_moves = self.inference_engine.infer_safe_moves(
            self.position, self.grabbed_gold, self.grabbed_HP, self.visited
        )
        print("=============================================================")
        return self.select_action(safe_moves)

    # Select an action based on the safe moves
    def select_action(
        self, safe_moves: List[Tuple[int, int]]
    ) -> List[Tuple[Action, int, int]]:
        # Select an action from safe moves
        print("============= Agent: Select Action =================")
        if not safe_moves:
            self.game_over = True
            return "end"
        else:
            next_position = safe_moves[0]
            self.current_action = []
            if (
                next_position == self.position
            ):  # It mean the current position contain gold or healing potion
                self.current_action.append(
                    (Action.GRAB, self.position[0], self.position[1])
                )
                print("=============> Current action: ", self.current_action)
                print("=============================================================")
                return self.current_action
            print("=============> Current position: ", self.position)
            print("=============> Current direction: ", self.current_direction)
            print("=============> Safe moves: ", safe_moves)
            print("=============> Next position: ", next_position)
            target_direction: Direction = get_target_direction(
                self.position, next_position
            )
            print("=============> Target direction: ", target_direction)
            turn_actions: List[Action] = get_actions(
                self.current_direction, target_direction
            )
            # Perform the turn left, turn right actions to align the direction
            self.current_action.extend(
                [
                    (action, self.position[0], self.position[1])
                    for action in turn_actions
                ]
            )
            print("=============> Current action: ", self.current_action)
            print("=============================================================")
            return self.current_action

    # Update the knowledge base with the new elements
    def update_knowledge(self, new_percept: Tuple[Percept, int, int]):
        self.knowledge_base.infer_new_knowledge()

    def is_game_over(self):
        return self.game_over

    def get_score(self):
        return self.score

    def handle_forward(self):
        self.position = ActionHandler.handle_forward(
            self.position, self.current_direction
        )
        print("Current position: ", self.position)

    def turn_left(self) -> Direction:
        print("Before turning left: ", self.current_direction)
        self.current_direction = ActionHandler.turn_left(self.current_direction)
        print("After turning left: ", self.current_direction)

    def turn_right(self) -> Direction:
        self.current_direction = ActionHandler.turn_right(self.current_direction)
        print("Current direction: ", self.current_direction)

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

        is_healing_potion = (
            self.inference_engine.infer_healing_potion(position)
            and position not in self.grabbed_HP
        )
        if is_healing_potion:
            self.grabbed_HP.add(position)
            self.healing_potions += 1

        is_gold = (
            self.inference_engine.infer_gold(position)
            and position not in self.grabbed_gold
        )
        if is_gold:
            self.score += 5000
            self.grabbed_gold.add(position)

    def heal(self):
        if self.healing_potions > 0:
            self.health = 100 if self.health + 25 > 100 else self.health + 25
            self.healing_potions -= 1

    def get_percept_string(self):
        percept_string = ""
        for percept in self.current_percepts:
            percept_string += f"{percept.name} "
        if not percept_string:
            percept_string = "None"
        return percept_string

    def get_action_string(self):
        action_string = ""
        for action in self.current_action:
            action_string += f"{action[0].name} "

        return action_string
