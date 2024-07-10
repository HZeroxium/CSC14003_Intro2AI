from citymap import CityMap
from utils import reconstruct_path, DIRECTIONS
import heapq
from typing import Dict, Set, List, Tuple


def ucs(city_map: CityMap) -> list[tuple]:
    start: Tuple[int, int] = city_map.start
    goal: Tuple[int, int] = city_map.goal
    frontier: List[Tuple[int, Tuple[int, int]]] = [(0, start)]
    visited: Set[Tuple[int, int]] = set()
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {start: None}
    cost: Dict[Tuple[int, int], int] = {start: 0}

    while frontier:
        current_cost, current = heapq.heappop(frontier)

        if city_map.is_goal(current):
            return reconstruct_path(parent, start, goal)

        if current in visited:
            continue

        visited.add(current)

        for direction in DIRECTIONS:
            next_cell = (current[0] + direction[0], current[1] + direction[1])
            if city_map.is_valid_move(next_cell):
                new_cost = current_cost + city_map.get_cost(current, next_cell)
                if next_cell not in cost or new_cost < cost[next_cell]:
                    cost[next_cell] = new_cost
                    heapq.heappush(frontier, (new_cost, next_cell))
                    parent[next_cell] = current

    return reconstruct_path(parent, start, goal)
