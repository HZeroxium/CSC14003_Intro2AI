from citymap import CityMap
from utils import reconstruct_path, DIRECTIONS, heuristic
from typing import Dict, Set, List, Tuple
import heapq


def gbfs(
    city_map: CityMap, start: Tuple[int, int], goal: Tuple[int, int]
) -> List[Tuple[int, int]]:
    frontier: List[Tuple[int, Tuple[int, int]]] = [(0, start)]
    visited: Set[Tuple[int, int]] = set()
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {start: None}

    while frontier:
        _, current = heapq.heappop(frontier)

        if city_map.is_goal(current):
            return reconstruct_path(parent, start, goal)

        if current in visited:
            continue

        visited.add(current)

        for direction in DIRECTIONS:
            next_cell = (current[0] + direction[0], current[1] + direction[1])
            if city_map.is_valid_move(next_cell) and next_cell not in visited:
                heapq.heappush(
                    frontier, (heuristic(next_cell, goal, city_map=city_map), next_cell)
                )
                parent[next_cell] = current

    return reconstruct_path(parent, start, goal)
