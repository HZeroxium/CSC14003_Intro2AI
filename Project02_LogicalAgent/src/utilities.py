# utilities.py

from enum import Enum
from typing import List, Tuple, Set, Dict


class Action(Enum):
    FORWARD = "forward"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    SHOOT = "shoot"
    GRAB = "grab"
    HEAL = "heal"
    CLIMB = "climb"


class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"


class Percept(Enum):
    BREEZE = "B"
    STENCH = "S"
    # SCREAM = "SC"
    WHIFF = "WF"
    GLOW = "GL"


class Element(Enum):
    AGENT = "A"
    WUMPUS = "W"
    GOLD = "G"
    PIT = "P"
    POISONOUS_GAS = "PG"
    HEALING_POTION = "HP"
    SAFE = None


ELEMENT_TO_PERCEPT: Dict[Element, Percept] = {
    Element.WUMPUS: Percept.STENCH,
    Element.PIT: Percept.BREEZE,
    Element.GOLD: Percept.GLOW,
    Element.POISONOUS_GAS: Percept.WHIFF,
    Element.AGENT: None,
    Element.HEALING_POTION: None,
}

PERCEPT_TO_ELEMENT: Dict[Percept, Element] = {
    Percept.STENCH: Element.WUMPUS,
    Percept.BREEZE: Element.PIT,
    Percept.GLOW: Element.GOLD,
    Percept.WHIFF: Element.POISONOUS_GAS,
}


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


class ActionHandler:
    @staticmethod
    def handle_forward(
        position: Tuple[int, int], direction: Direction
    ) -> Tuple[int, int]:
        x, y = position
        if direction == Direction.NORTH:
            return (x - 1, y)
        elif direction == Direction.SOUTH:
            return (x + 1, y)
        elif direction == Direction.WEST:
            return (x, y - 1)
        elif direction == Direction.EAST:
            return (x, y + 1)

    @staticmethod
    def turn_left(direction: Direction) -> Direction:
        if direction == Direction.NORTH:
            return Direction.WEST
        elif direction == Direction.SOUTH:
            return Direction.EAST
        elif direction == Direction.WEST:
            return Direction.SOUTH
        elif direction == Direction.EAST:
            return Direction.NORTH

    @staticmethod
    def turn_right(direction: Direction) -> Direction:
        if direction == Direction.NORTH:
            return Direction.EAST
        elif direction == Direction.SOUTH:
            return Direction.WEST
        elif direction == Direction.WEST:
            return Direction.NORTH
        elif direction == Direction.EAST:
            return Direction.SOUTH

    @staticmethod
    def handle_shoot(
        position: Tuple[int, int], direction: Direction
    ) -> Tuple[int, int]:
        return ActionHandler.handle_forward(position, direction)
