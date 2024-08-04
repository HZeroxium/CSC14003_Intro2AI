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

    # Main function to choose the next action
    def choose_action(
        self,
        percepts: List[Tuple[Percept, int, int]],
        element: Tuple[Element, int, int],
    ) -> str:
        # Check if current position is visited (it means the agent is back to the parent node)
        if self.position not in self.visited:
            self.visited.add(self.position)
            print("Visited: ", self.visited)
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
            self.inference_engine.infer_not_percepts(
                self.position, self.current_percepts
            )
            # Use inference to decide the next action
            self.knowledge_base.update(percepts)
            print("=============================================================")
        safe_moves = self.inference_engine.infer_safe_moves(
            self.position,
            self.grabbed_gold,
            self.grabbed_HP,
            self.visited,
            self.dangerous_cells,
        )
        return self.select_action(safe_moves)

    # Select an action based on the safe moves
    def select_action(
        self, safe_moves: List[Tuple[int, int]]
    ) -> List[Tuple[Action, int, int]]:
        self.current_action = []
        is_back = False
        # Select an action from safe moves
        print("============= Agent: Select Action =================")
        next_position = None
        if not safe_moves:
            # Check if all map is visited
            if len(self.visited) == self.grid_size * self.grid_size:
                self.game_over = True
                return "end"
            # If there is no safe move, then go back to the parent node and explore other paths
            next_position = self.parent[self.position]
            is_back = True
            # self.game_over = True
            # return "end"
        else:
            next_position = safe_moves[0]
            if (
                next_position == self.position
            ):  # It mean the current position contain gold or healing potion
                next_position = safe_moves[1]
                self.current_action.append(
                    (Action.GRAB, self.position[0], self.position[1])
                )
                print("=============> Current action: ", self.current_action)
                print("=============================================================")
                # return self.current_action
        if not is_back:
            self.parent[next_position] = self.position
        target_direction: Direction = get_target_direction(self.position, next_position)
        print("=====> Parent of ", next_position, " is ", self.parent[next_position])
        print("=============> Current position: ", self.position)
        print("=============> Current direction: ", self.current_direction)
        print("=============> Next position: ", next_position)
        print("=============> Target direction: ", target_direction)
        print("=============> Current action: ", self.current_action)
        turn_actions: List[Action] = get_actions(
            self.current_direction, target_direction
        )
        # Perform the turn left, turn right actions to align the direction
        self.current_action.extend(
            [(action, self.position[0], self.position[1]) for action in turn_actions]
        )
        if next_position == INITIAL_POSITION:
            self.current_action.append(
                (Action.CLIMB, self.position[0], self.position[1])
            )
        print("=============================================================")
        return self.current_action

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
        print("Current position: ", self.position)

    def turn_left(self) -> Direction:
        self.score -= 10
        print("Before turning left: ", self.current_direction)
        self.current_direction = ActionHandler.turn_left(self.current_direction)
        print("After turning left: ", self.current_direction)

    def turn_right(self) -> Direction:
        self.score -= 10
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
        self.score -= 10
        if self.healing_potions > 0:
            self.health = 100 if self.health + 25 > 100 else self.health + 25
            self.healing_potions -= 1

    def handle_climb(self):
        self.score += 10
        if self.position == INITIAL_POSITION:
            self.game_won = True

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

    def get_dangerous_cells_str(self):
        # Get the string representation of dangerous cells
        dangerous_cells_str = ""
        for element, x, y in self.dangerous_cells:
            dangerous_cells_str += f"({element.value}, {x}, {y}),"
        return dangerous_cells_str
