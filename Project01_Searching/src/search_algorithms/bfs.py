from collections import deque
from citymap import CityMap
from utils import reconstruct_path, DIRECTIONS

from typing import Dict, Tuple, List, Set


def bfs(city_map: CityMap) -> List[Tuple[int, int]]:
    start, goal = city_map.start, city_map.goal
    frontier = deque([start])

    visited: Set[Tuple[int, int]] = Set()
    visited.add(start)
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {start: None}

    while frontier:
        current = frontier.popleft()

        if city_map.is_goal(current):
            return reconstruct_path(parent, start, goal)

        for direction in DIRECTIONS:
            next_cell = (current[0] + direction[0], current[1] + direction[1])
            if city_map.is_valid_move(next_cell) and next_cell not in visited:
                frontier.append(next_cell)
                visited.add(next_cell)
                parent[next_cell] = current

    return reconstruct_path(parent, start, goal)
