# agent.py

from knowledge_base import KnowledgeBase
from inference_engine import InferenceEngine
from typing import Tuple, List, Set
from utilities import Action, Direction, Percept, Element


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

    # Main function to choose the next action
    def choose_action(
        self,
        percepts: List[Tuple[Percept, int, int]],
        elements: Tuple[Element, int, int],
    ) -> str:
        # Update the current percepts
        self.visited.add(self.position)
        self.current_percepts.clear()
        for percept, x, y in percepts:
            self.current_percepts.add(percept)
        print("============= Agent: Choose Action =================")
        # print("=============> Current percepts: ", self.current_percepts)
        print("=============> Current elements: ", elements)
        # Update the knowledge base with the new elements if elements is not None
        if elements is not None:
            self.knowledge_base.add_clause(
                [self.knowledge_base.encode(elements[0], elements[1], elements[2])]
            )
            print("=============> Add ", elements[0], " at ", elements[1], elements[2])

        # Infer that there is no element except the current element at the current position
        for element in Element:
            if element == Element.SAFE or element == Element.AGENT:
                continue
            encode_element = -self.knowledge_base.encode(
                element, self.position[0], self.position[1]
            )
            if (
                self.knowledge_base.query(encode_element) and element != elements[0]
                if elements is not None
                else True
            ):
                not_element_clause = [
                    -self.knowledge_base.encode(
                        element, self.position[0], self.position[1]
                    )
                ]
                self.knowledge_base.add_clause(not_element_clause)
                print("=============> Not ", element, " at ", self.position)
        # Get percepts that not exists in percepts
        for percept in Percept:
            if percept not in self.current_percepts and percept != Percept.SCREAM:
                print("=============> Add not ", percept, " at ", self.position)
                self.knowledge_base.add_clause(
                    [
                        -self.knowledge_base.encode(
                            percept, self.position[0], self.position[1]
                        )
                    ]
                )
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
            # self.current_direction = target_direction
            # print("=============> Current position: ", self.position)
            # print("=============> Current direction: ", self.current_direction)
            # Reset the current action

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
        if new_percept is None:
            return
        # Update the knowledge base with the new percept (Percept.SCREAM)
        percept, x, y = new_percept
        if percept == Percept.SCREAM:
            # If there is a scream, it means the Wumpus is killed with a shoot at current position and direction
            # Get Wumpus position
            if self.current_direction == Direction.NORTH:
                wumpus_position = (x + 1, y)
            elif self.current_direction == Direction.SOUTH:
                wumpus_position = (x - 1, y)
            elif self.current_direction == Direction.WEST:
                wumpus_position = (x, y + 1)
            elif self.current_direction == Direction.EAST:
                wumpus_position = (x, y - 1)
            # Remove the Wumpus from the knowledge base
            not_wumpus_clause = [
                -self.knowledge_base.encode(
                    Element.WUMPUS, wumpus_position[0], wumpus_position[1]
                )
            ]
            self.knowledge_base.add_clause(not_wumpus_clause)

        self.knowledge_base.infer_new_knowledge()

    def log_action(self, action):
        # Log the action taken
        print(f"Action taken: {action}")

    def is_game_over(self):
        return self.game_over

    def get_score(self):
        return self.score

    def handle_forward(self, position: Tuple[int, int]):
        # Move forward from the current position with current direction
        print("Current direction: ", self.current_direction)
        if self.current_direction == Direction.NORTH:  # Move up
            self.position = (position[0] - 1, position[1])
        elif self.current_direction == Direction.SOUTH:  # Move down
            self.position = (position[0] + 1, position[1])
        elif self.current_direction == Direction.WEST:  # Move left
            self.position = (position[0], position[1] - 1)
        elif self.current_direction == Direction.EAST:  # Move right
            self.position = (position[0], position[1] + 1)

    def turn_left(self, direction: Direction) -> Direction:
        if direction == Direction.NORTH:
            return Direction.WEST
        elif direction == Direction.SOUTH:
            return Direction.EAST
        elif direction == Direction.WEST:
            return Direction.SOUTH
        elif direction == Direction.EAST:
            return Direction.NORTH

    def turn_right(self, direction: Direction) -> Direction:
        if direction == Direction.NORTH:
            return Direction.EAST
        elif direction == Direction.SOUTH:
            return Direction.WEST
        elif direction == Direction.WEST:
            return Direction.NORTH
        elif direction == Direction.EAST:
            return Direction.SOUTH

    def handle_shoot(self, position: Tuple[int, int]):
        self.score -= 100

    def handle_grab(self, position: Tuple[int, int]):
        is_healing_potion = (
            self.inference_engine.infer_healing_potion(position)
            and position not in self.grabbed_HP
        )
        if is_healing_potion:
            self.health += 25
            # Remove the healing potion from the knowledge base
            # not_hp_clause = [
            #     -self.knowledge_base.encode(
            #         Element.HEALING_POTION, position[0], position[1]
            #     )
            # ]
            # self.knowledge_base.add_clause(not_hp_clause)
            self.grabbed_HP.add(position)

        self.score -= 10

        is_gold = (
            self.inference_engine.infer_gold(position)
            and position not in self.grabbed_gold
        )
        if is_gold:
            self.score += 5000
            # not_gold_clause = [
            #     -self.knowledge_base.encode(Element.GOLD, position[0], position[1])
            # ]
            # self.knowledge_base.add_clause(not_gold_clause)
            self.grabbed_gold.add(position)
        self.score -= 10

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


# Helper function to get list of actions based on the current direction and the target direction
def get_actions(
    current_direction: Direction, target_direction: Direction
) -> List[Action]:
    actions = []
    if current_direction == target_direction:
        actions.append(Action.FORWARD)
    else:
        if current_direction == Direction.NORTH:
            if target_direction == Direction.WEST:
                actions.append(Action.TURN_LEFT)
            elif target_direction == Direction.EAST:
                actions.append(Action.TURN_RIGHT)
            elif target_direction == Direction.SOUTH:
                actions.append(Action.TURN_LEFT)
                actions.append(Action.TURN_LEFT)
        elif current_direction == Direction.SOUTH:
            if target_direction == Direction.WEST:
                actions.append(Action.TURN_RIGHT)
            elif target_direction == Direction.EAST:
                actions.append(Action.TURN_LEFT)
            elif target_direction == Direction.NORTH:
                actions.append(Action.TURN_LEFT)
                actions.append(Action.TURN_LEFT)
        elif current_direction == Direction.WEST:
            if target_direction == Direction.NORTH:
                actions.append(Action.TURN_RIGHT)
            elif target_direction == Direction.SOUTH:
                actions.append(Action.TURN_LEFT)
            elif target_direction == Direction.EAST:
                actions.append(Action.TURN_LEFT)
                actions.append(Action.TURN_LEFT)
        elif current_direction == Direction.EAST:
            if target_direction == Direction.NORTH:
                actions.append(Action.TURN_LEFT)
            elif target_direction == Direction.SOUTH:
                actions.append(Action.TURN_RIGHT)
            elif target_direction == Direction.WEST:
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
            return Direction.EAST
        else:
            return Direction.WEST
    elif y1 == y2:
        if x2 > x1:
            return Direction.SOUTH
        else:
            return Direction.NORTH
