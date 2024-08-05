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

# Constants
INITIAL_POSITION = (0, 0)  # Initial position of the agent
INITIAL_HEALTH = 100  # Initial health of the agent
GRID_DEFAULT_SIZE = 4  # Default grid size for the agent
SCORE_PENALTY_MOVE = 10  # Score penalty for moving or turning
SCORE_PENALTY_SHOOT = 100  # Score penalty for shooting
SCORE_REWARD_GOLD = 5000  # Score reward for grabbing gold
SCORE_REWARD_CLIMB = 10  # Score reward for climbing
HEALTH_MAXIMUM = 100  # Maximum health the agent can have
HEALTH_INCREASE_POTION = 25  # Health increase per healing potion
LOG_FILE_NAME = "actions.log"  # Log file name for actions

# Agent class to represent the agent in the Wumpus World
class Agent:
    def __init__(
        self,
        initial_position: Tuple[int, int] = INITIAL_POSITION,
        health: int = INITIAL_HEALTH,
        grid_size: int = GRID_DEFAULT_SIZE,
    ):
        # Initialize the knowledge base
        self.knowledge_base = KnowledgeBase(grid_size=grid_size)
        
        # Initialize the inference engine
        self.inference_engine = InferenceEngine(knowledge_base=self.knowledge_base)
        
        # Initial setup for the agent
        self.position = initial_position  # Current position of the agent
        self.health = health  # Health of the agent
        self.grid_size = grid_size  # Size of the grid
        self.score = 0  # Score of the agent
        self.game_over = False  # Flag to indicate if the game is over
        self.game_won = False  # Flag to indicate if the game is won
        self.current_direction = Direction.NORTH  # Current direction of the agent
        self.current_percepts: Set[Percept] = set()  # Current percepts of the agent
        self.current_action: List[Tuple[Action, int, int]] = []  # Current action of the agent
        self.grabbed_gold: Set[Tuple[int, int]] = set()  # Set of grabbed gold
        self.grabbed_HP: Set[Tuple[int, int]] = set()  # Set of grabbed healing potions
        self.visited: Set[Tuple[int, int]] = set()  # Set of visited cells
        self.parent: Dict[Tuple[int, int], Tuple[int, int]] = {}  # Parent dictionary to store the parent of each cell
        self.healing_potions: int = 0  # Number of healing potions grabbed
        self.dangerous_cells: Set[Tuple[Element, int, int]] = set()  # Set of dangerous cells

    def get_data(self) -> str:
        """
        Return a string with relevant agent data for display
        """
        return f"Position: {self.position}, Health: {self.health}, Score: {self.get_score()}"

    # Main function to choose the next action
    def choose_action(
        self,
        percepts: List[Tuple[Percept, int, int]],
        element: Tuple[Element, int, int],
    ) -> str:
        """
        Determine the next action based on percepts and elements in the current position
        """
        # Check if current position is visited (it means the agent is back to the parent node)
        if self.position not in self.visited:
            self.visited.add(self.position)
            self.current_percepts.clear()
            for percept, x, y in percepts:
                self.current_percepts.add(percept)

            # Update the inference engine with current position elements and percepts
            self.inference_engine.add_element(self.position, element[0])
            self.inference_engine.infer_not_elements(self.position, element[0])
            self.inference_engine.infer_not_percepts(self.position, self.current_percepts)

            # Update knowledge base with new percepts
            self.knowledge_base.update(percepts)

        # Infer safe moves and select an action
        safe_moves = self._infer_safe_moves()
        return self._select_action(safe_moves)

    # Update the knowledge base with the new elements
    def update_knowledge(self, new_percept: Tuple[Percept, int, int]):
        """
        Infer new knowledge based on new percepts
        """
        self.knowledge_base.infer_new_knowledge()

    def is_game_over(self) -> bool:
        """
        Check if the game is over
        """
        return self.game_over

    def is_game_won(self) -> bool:
        """
        Check if the game is won
        """
        return self.game_won

    def get_score(self) -> int:
        """
        Get the current score of the agent
        """
        return self.score

    def handle_forward(self):
        """
        Handle moving the agent forward
        """
        self.score -= SCORE_PENALTY_MOVE
        self.position = ActionHandler.handle_forward(self.position, self.current_direction)

    def turn_left(self) -> Direction:
        """
        Handle turning the agent left
        """
        self.score -= SCORE_PENALTY_MOVE
        self.current_direction = ActionHandler.turn_left(self.current_direction)

    def turn_right(self) -> Direction:
        """
        Handle turning the agent right
        """
        self.score -= SCORE_PENALTY_MOVE
        self.current_direction = ActionHandler.turn_right(self.current_direction)

    def handle_shoot(self, is_killed: bool):
        """
        Handle shooting action and update knowledge base if Wumpus is killed
        """
        self.score -= SCORE_PENALTY_SHOOT
        shoot_position = ActionHandler.handle_forward(self.position, self.current_direction)
        
        if is_killed:
            self.knowledge_base.add_clause([
                -self.knowledge_base.encode(Element.WUMPUS, shoot_position[0], shoot_position[1])
            ])

    def handle_grab(self, position: Tuple[int, int]):
        """
        Handle grabbing items (gold or healing potions) in the current position
        """
        self.score -= SCORE_PENALTY_MOVE
        
        if self._is_healing_potion(position):
            self.grabbed_HP.add(position)
            self.healing_potions += 1
        
        if self._is_gold(position):
            self.score += SCORE_REWARD_GOLD
            self.grabbed_gold.add(position)

    def _is_healing_potion(self, position: Tuple[int, int]) -> bool:
        """
        Check if there is a healing potion at the specified position
        """
        return self.inference_engine.infer_healing_potion(position) and position not in self.grabbed_HP

    def _is_gold(self, position: Tuple[int, int]) -> bool:
        """
        Check if there is gold at the specified position
        """
        return self.inference_engine.infer_gold(position) and position not in self.grabbed_gold

    def heal(self):
        """
        Handle healing the agent using available healing potions
        """
        self.score -= SCORE_PENALTY_MOVE
        if self.healing_potions > 0:
            self.health = min(HEALTH_MAXIMUM, self.health + HEALTH_INCREASE_POTION)
            self.healing_potions -= 1

    def handle_climb(self):
        """
        Handle climbing action, mark game as won if agent is at the initial position
        """
        self.score += SCORE_REWARD_CLIMB
        if self.position == INITIAL_POSITION:
            self.game_won = True

    def get_percept_string(self) -> str:
        """
        Get a string representation of the current percepts
        Format: (Percept1, Percept2, ...)
        """
        return ", ".join(percept.name for percept in self.current_percepts) or "None"

    def get_action_string(self) -> str:
        """
        Get a string representation of the current actions
        Format: [Action1, Action2, ...]. Example: [TURN_LEFT, FORWARD, GRAB]
        """
        return ", ".join(action.name for action, _, _ in self.current_action) or "None"

    def get_dangerous_cells_str(self) -> str:
        """
        Get a string representation of dangerous cells
        """
        return ", ".join(f"({element.value}, {x}, {y})" for element, x, y in self.dangerous_cells)

    def _infer_safe_moves(self) -> List[Tuple[int, int]]:
        """
        Infer safe moves using the inference engine
        """
        return self.inference_engine.infer_safe_moves(
            self.position,
            self.grabbed_gold,
            self.grabbed_HP,
            self.visited,
            self.dangerous_cells,
        )

    def _select_action(self, safe_moves: List[Tuple[int, int]]) -> str:
        """
        Select the next action based on inferred safe moves
        """
        self.current_action = []
        
        if not safe_moves:
            return self._handle_no_safe_moves()
        
        return self._handle_safe_moves(safe_moves)

    def _handle_no_safe_moves(self) -> str:
        """
        Handle scenario when there are no safe moves
        """
        if len(self.visited) == self.grid_size * self.grid_size:
            self.game_over = True
            return "end"
        
        next_position = self.parent[self.position]
        self._move_to_position(next_position, is_back=True)
        return self.current_action

    def _handle_safe_moves(self, safe_moves: List[Tuple[int, int]]) -> str:
        """
        Handle scenario when there are safe moves
        """
        next_position = safe_moves[0]
        
        if next_position == self.position:
            next_position = safe_moves[1]
            self.current_action.append((Action.GRAB, self.position[0], self.position[1]))
        
        self._move_to_position(next_position)
        
        if next_position == INITIAL_POSITION:
            self.current_action.append((Action.CLIMB, INITIAL_POSITION[0], INITIAL_POSITION[1]))
        
        return self.current_action

    def _move_to_position(self, next_position: Tuple[int, int], is_back: bool = False):
        """
        Move the agent to the specified position
        """
        if not is_back:
            self.parent[next_position] = self.position
        
        target_direction = get_target_direction(self.position, next_position)
        turn_actions = get_actions(self.current_direction, target_direction)
        
        self.current_action.extend(
            [(action, self.position[0], self.position[1]) for action in turn_actions]
        )

    def log_actions(self):
        """
        Write action to log file with format:
        (x, y): action_name
        """
        with open(LOG_FILE_NAME, "a") as f:
            for action, x, y in self.current_action:
                f.write(f"({x}, {y}): {action.name}\n")
