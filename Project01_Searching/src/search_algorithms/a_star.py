from citymap import CityMap
from utils import reconstruct_path, DIRECTIONS, heuristic
import heapq
from typing import Dict, Set, List, Tuple


def astar(city_map: CityMap) -> List[Tuple[int, int]]:
    start: Tuple[int, int] = city_map.start
    goal: Tuple[int, int] = city_map.goal
    frontier: List[Tuple[int, Tuple[int, int]]] = [(0, start)]
    visited: Set[Tuple[int, int]] = set()
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {start: None}
    g_cost: Dict[Tuple[int, int], int] = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if city_map.is_goal(current):
            return reconstruct_path(parent, start, goal)

        if current in visited:
            continue

        visited.add(current)

        for direction in DIRECTIONS:
            next_cell = (current[0] + direction[0], current[1] + direction[1])
            if city_map.is_valid_move(next_cell):
                tentative_g_cost = g_cost[current] + city_map.get_cost(
                    current, next_cell
                )
                if next_cell not in g_cost or tentative_g_cost < g_cost[next_cell]:
                    g_cost[next_cell] = tentative_g_cost
                    f_cost = tentative_g_cost + heuristic(next_cell, goal)
                    heapq.heappush(
                        frontier,
                        (f_cost, next_cell),
                    )
                    parent[next_cell] = current

    return reconstruct_path(parent, start, goal)
