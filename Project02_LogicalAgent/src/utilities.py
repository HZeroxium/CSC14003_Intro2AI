# utilities.py

from enum import Enum
from typing import List, Tuple, Set, Dict


class Action(Enum):
    FORWARD = "forward"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    SHOOT = "shoot"
    GRAB = "grab"


class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"


class Percept(Enum):
    BREEZE = "B"
    STENCH = "S"
    SCREAM = "SC"
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
