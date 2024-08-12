# File: ./src/agent.py

# This file defines the `Agent` class for the "Wumpus World" game.
# It handles the agent's movements, actions, and interactions with the game environment.
# The agent maintains a knowledge base and inference engine to make decisions based on percepts and environment elements.
# Key functionalities include determining the next action, updating the agent's knowledge, handling movement,
# grabbing items, shooting, and logging actions. It also includes logic for finding safe moves and paths within the game grid.

# main.py
#     └─game.py
#           ├──agent.py <-------------------------------------------
#           │      └──inference_engine.py
#           │             ├── knowledge_base.py
#           │             │       ├── utilities.py
#           │             │       ├── pysat.formula (external)
#           │             │       └── pysat.solvers (external)
#           │             └── utilities.py
#           ├──environment.py
#           │      └──utilities.py
#           ├──graphics_manager.py
#           │      ├──utilities.py
#           │      └──info_panel_graphics.py
#           │             └── pygame (external)
#           └── pygame (external)

from inference_engine import InferenceEngine, KnowledgeBase, get_adjacent_cells
from typing import Tuple, List, Set, Dict, Optional
from utilities import (
    Action,
    Direction,
    Percept,
    Element,
    get_actions,
    get_target_direction,
    ActionHandler,
)

from collections import deque
import heapq

# Constants
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
        initial_position: Tuple[int, int],
        health: int = INITIAL_HEALTH,
        grid_size: int = GRID_DEFAULT_SIZE,
    ):
        # Initialize the knowledge base
        self.knowledge_base = KnowledgeBase(grid_size=grid_size)

        # Initialize the inference engine
        self.inference_engine = InferenceEngine(knowledge_base=self.knowledge_base)

        # Initial setup for the agent
        self.start_position = initial_position  # Initial position of the agent
        self.position = initial_position  # Current position of the agent
        self.health = health  # Health of the agent
        self.grid_size = grid_size  # Size of the grid
        self.score = 0  # Score of the agent
        self.game_over = False  # Flag to indicate if the game is over
        self.be_eaten = False  # Flag to indicate if the agent is eater by th Wumpus
        self.fall_down = False  # Flag to indicate if the agent falls into a pit
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
            self.inference_engine.infer_not_percepts(
                self.position, self.current_percepts
            )

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
        self.knowledge_base.infer_new_knowledge(self.dangerous_cells)

    def is_game_over(self) -> bool:
        """
        Check if the game is over
        """
        if self.health == 0:
            self.game_over = True

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
        self.position = ActionHandler.handle_forward(
            self.position, self.current_direction
        )

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
        """
        Handle grabbing items (gold or healing potions) in the current position
        """
        self.score -= SCORE_PENALTY_MOVE

        if self._is_healing_potion(position):
            self.grabbed_HP.add(position)
            self.healing_potions += 1
            self.heal()

        if self._is_gold(position):
            self.score += SCORE_REWARD_GOLD
            self.grabbed_gold.add(position)

    def _is_healing_potion(self, position: Tuple[int, int]) -> bool:
        """
        Check if there is a healing potion at the specified position
        """
        return (
            self.inference_engine.infer_healing_potion(position)
            and position not in self.grabbed_HP
        )

    def _is_gold(self, position: Tuple[int, int]) -> bool:
        """
        Check if there is gold at the specified position
        """
        return (
            self.inference_engine.infer_gold(position)
            and position not in self.grabbed_gold
        )

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
        if self.position == self.start_position:
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
        return ", ".join(
            f"({element.value}, {x}, {y})" for element, x, y in self.dangerous_cells
        )

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
            self.start_position,
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
        nearest_unvisited_neighbor = None
        # Union of visited cells and dangerous cells is equal to the total number of cells
        dangerous_cells: Set[Tuple[int, int]] = set()
        for element, x, y in self.dangerous_cells:
            dangerous_cells.add((x, y))
        if len(self.visited.union(dangerous_cells)) == self.grid_size * self.grid_size:
            adjacent_cells = get_adjacent_cells(
                self.start_position[0], self.start_position[1], self.grid_size
            )

            # Find the nearest and safe cell to move back
            smallest_distance = float("inf")
            for cell in adjacent_cells:
                if self._is_safe_move(cell):
                    distance = abs(cell[0] - self.position[0]) + abs(
                        cell[1] - self.position[1]
                    )
                    if distance < smallest_distance:
                        smallest_distance = distance
                        nearest_unvisited_neighbor = cell

        else:
            nearest_unvisited_neighbor = self._find_nearest_unvisited_neighbor()
            print("Nearest unvisited neighbor:", nearest_unvisited_neighbor)
        if nearest_unvisited_neighbor is None:
            next_position = self.parent[self.position]
        else:
            path = self._find_path_to_safe_cell_near(nearest_unvisited_neighbor)
            print("Path to", nearest_unvisited_neighbor, ":", path)
            next_position = path[1] if len(path) > 1 else path[0]

        self._move_to_position(next_position)
        return self.current_action

    def _handle_safe_moves(self, safe_moves: List[Tuple[int, int]]) -> str:
        """
        Handle scenario when there are safe moves
        """
        next_position = safe_moves[0]

        if len(safe_moves) > 1 and next_position == self.position:
            next_position = safe_moves[1]
            self.current_action.append(
                (Action.GRAB, self.position[0], self.position[1])
            )

        self._move_to_position(next_position)

        if next_position == self.start_position:
            self.current_action.append(
                (Action.CLIMB, self.start_position[0], self.start_position[1])
            )

        return self.current_action

    def _is_position_within_bounds(self, position):
        x, y = position
        return (
            0 <= x < self.environment.get_map_size()
            and 0 <= y < self.environment.get_map_size()
        )

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

    def _find_nearest_unvisited(self) -> Tuple[int, int]:
        min_distance = float("inf")
        nearest_position = None
        dangerous_cells: Set[Tuple[int, int]] = set()

        for element, x, y in self.dangerous_cells:
            dangerous_cells.add((x, y))
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if (row, col) not in self.visited and (
                    row,
                    col,
                ) not in dangerous_cells:
                    distance = abs(row - self.position[0]) + abs(col - self.position[1])
                    if distance < min_distance:
                        min_distance = distance
                        nearest_position = (row, col)

        return nearest_position

    def _find_path_to_safe_cell_near(
        self, target: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
            # Hàm heuristic sử dụng khoảng cách Manhattan
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        start = self.position
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current_priority, current = heapq.heappop(frontier)

            if current == target:
                # Tìm thấy ô mục tiêu, xây dựng đường đi và trả về
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            neighbors = self._get_neighbors(current)
            for neighbor in neighbors:
                if neighbor in self.visited:  # Chỉ xét các ô đã được visited
                    new_cost = cost_so_far[current] + 1
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        priority = new_cost + heuristic(neighbor, target)
                        heapq.heappush(frontier, (priority, neighbor))
                        came_from[neighbor] = current

        # Trường hợp không tìm thấy đường đi, trả về danh sách rỗng
        return []

    def _get_neighbors(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        neighbors = []
        x, y = position
        if x > 0:
            neighbors.append((x - 1, y))
        if x < self.grid_size - 1:
            neighbors.append((x + 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
        if y < self.grid_size - 1:
            neighbors.append((x, y + 1))
        return neighbors

    def _is_safe_move(self, position: Tuple[int, int]) -> bool:
        return position in self.visited and position not in self.dangerous_cells

    def _find_neighboring_visited_cells(self) -> List[Tuple[int, int]]:
        neighboring_visited = []
        dangerous_cells = set((x, y) for element, x, y in self.dangerous_cells)

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if (row, col) not in self.visited and (row, col) not in dangerous_cells:
                    neighbors = self._get_neighbors((row, col))
                    for neighbor in neighbors:
                        if neighbor in self.visited and neighbor not in dangerous_cells:
                            neighboring_visited.append(neighbor)

        return neighboring_visited

    def _find_nearest_unvisited_neighbor(self) -> Optional[Tuple[int, int]]:
        neighboring_visited = self._find_neighboring_visited_cells()
        min_distance = float("inf")
        nearest_position = None

        for cell in neighboring_visited:
            distance = abs(cell[0] - self.position[0]) + abs(cell[1] - self.position[1])
            if distance < min_distance:
                min_distance = distance
                nearest_position = cell

        return nearest_position
