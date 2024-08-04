from enum import Enum
from typing import List, Tuple, Dict


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


def get_target_direction(
    current_position: Tuple[int, int], target_position: Tuple[int, int]
) -> Direction:
    x1, y1 = current_position
    x2, y2 = target_position
    if x1 == x2:
        return Direction.EAST if y2 > y1 else Direction.WEST
    if y1 == y2:
        return Direction.SOUTH if x2 > x1 else Direction.NORTH


def get_actions(
    current_direction: Direction, target_direction: Direction
) -> List[Action]:
    actions = []
    if current_direction == target_direction:
        actions.append(Action.FORWARD)
    else:
        actions.extend(determine_turn_actions(current_direction, target_direction))
        actions.append(Action.FORWARD)
    return actions


def determine_turn_actions(
    current_direction: Direction, target_direction: Direction
) -> List[Action]:
    if current_direction == Direction.NORTH:
        if target_direction == Direction.WEST:
            return [Action.TURN_LEFT]
        if target_direction == Direction.EAST:
            return [Action.TURN_RIGHT]
        if target_direction == Direction.SOUTH:
            return [Action.TURN_LEFT, Action.TURN_LEFT]
    if current_direction == Direction.SOUTH:
        if target_direction == Direction.WEST:
            return [Action.TURN_RIGHT]
        if target_direction == Direction.EAST:
            return [Action.TURN_LEFT]
        if target_direction == Direction.NORTH:
            return [Action.TURN_LEFT, Action.TURN_LEFT]
    if current_direction == Direction.WEST:
        if target_direction == Direction.NORTH:
            return [Action.TURN_RIGHT]
        if target_direction == Direction.SOUTH:
            return [Action.TURN_LEFT]
        if target_direction == Direction.EAST:
            return [Action.TURN_LEFT, Action.TURN_LEFT]
    if current_direction == Direction.EAST:
        if target_direction == Direction.NORTH:
            return [Action.TURN_LEFT]
        if target_direction == Direction.SOUTH:
            return [Action.TURN_RIGHT]
        if target_direction == Direction.WEST:
            return [Action.TURN_LEFT, Action.TURN_LEFT]
    return []


class ActionHandler:
    @staticmethod
    def handle_forward(
        position: Tuple[int, int], direction: Direction
    ) -> Tuple[int, int]:
        x, y = position
        if direction == Direction.NORTH:
            return (x - 1, y)
        if direction == Direction.SOUTH:
            return (x + 1, y)
        if direction == Direction.WEST:
            return (x, y - 1)
        if direction == Direction.EAST:
            return (x, y + 1)

    @staticmethod
    def turn_left(direction: Direction) -> Direction:
        return {
            Direction.NORTH: Direction.WEST,
            Direction.SOUTH: Direction.EAST,
            Direction.WEST: Direction.SOUTH,
            Direction.EAST: Direction.NORTH,
        }[direction]

    @staticmethod
    def turn_right(direction: Direction) -> Direction:
        return {
            Direction.NORTH: Direction.EAST,
            Direction.SOUTH: Direction.WEST,
            Direction.WEST: Direction.NORTH,
            Direction.EAST: Direction.SOUTH,
        }[direction]

    @staticmethod
    def handle_shoot(
        position: Tuple[int, int], direction: Direction
    ) -> Tuple[int, int]:
        return ActionHandler.handle_forward(position, direction)
