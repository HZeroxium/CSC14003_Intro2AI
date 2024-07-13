from citymap import CityMap, CellType
from utils import reconstruct_path, DIRECTIONS, heuristic, heuristic_2
import heapq
from typing import Dict, Set, List, Tuple


def a_star(city_map: CityMap, level: int = 1) -> List[Tuple[int, int]]:
    start: Tuple[int, int] = city_map.start
    goal: Tuple[int, int] = city_map.goal
    frontier: List[Tuple[int, Tuple[int, int]]] = [(0, start)]
    visited: Set[Tuple[int, int]] = set()
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {start: None}
    g_cost: Dict[Tuple[int, int], int] = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if city_map.is_goal(current):
            if level == 2:
                if g_cost[current] <= city_map.delivery_time:
                    return reconstruct_path(parent, start, goal)
                else:
                    return None
            return reconstruct_path(parent, start, goal)

        if current in visited:
            continue

        visited.add(current)

        for direction in DIRECTIONS:
            next_cell = (current[0] + direction[0], current[1] + direction[1])
            if city_map.is_valid_move(next_cell):
                tentative_g_cost = g_cost[current] + city_map.get_cost(next_cell)
                if next_cell not in g_cost or tentative_g_cost < g_cost[next_cell]:
                    g_cost[next_cell] = tentative_g_cost
                    f_cost = tentative_g_cost + heuristic(next_cell, goal)
                    heapq.heappush(
                        frontier,
                        (f_cost, next_cell),
                    )
                    parent[next_cell] = current

    return reconstruct_path(parent, start, goal)


def a_star_2(city_map: CityMap, level: int = 1) -> List[Tuple[int, int]]:
    start: Tuple[int, int] = city_map.start
    goal: Tuple[int, int] = city_map.goal
    frontier: List[Tuple[int, Tuple[int, int], int]] = [(0, start, city_map.fuel)]
    visited: Set[Tuple[int, int, int]] = set()
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {start: None}
    g_cost: Dict[Tuple[int, int], int] = {start: 0}

    while frontier:
        _, current, current_fuel = heapq.heappop(frontier)

        if city_map.is_goal(current):
            if level >= 2:
                if g_cost[current] <= city_map.delivery_time:
                    return reconstruct_path(parent, start, goal)
                else:
                    return None
            return reconstruct_path(parent, start, goal)

        if (current, current_fuel) in visited:
            continue

        visited.add((current, current_fuel))

        for direction in DIRECTIONS:
            next_cell = (current[0] + direction[0], current[1] + direction[1])
            if city_map.is_valid_move(next_cell):
                next_fuel = current_fuel - 1
                if next_fuel < 0:
                    continue  # Not enough fuel to move to the next cell

                tentative_g_cost = g_cost[current] + city_map.get_cost(next_cell)
                if city_map.get_cell(next_cell).type == CellType.FUEL_STATION:
                    next_fuel = city_map.fuel_capacity  # Refill fuel

                if next_cell not in g_cost or tentative_g_cost < g_cost[next_cell]:
                    g_cost[next_cell] = tentative_g_cost
                    f_cost = tentative_g_cost + heuristic_2(
                        next_cell, goal, city_map, next_fuel
                    )
                    heapq.heappush(
                        frontier,
                        (f_cost, next_cell, next_fuel),
                    )
                    parent[next_cell] = current

    return None


def a_star_3(
    city_map: CityMap,
    start: Tuple[int, int],
    goal: Tuple[int, int],
    fuel: int,
    level: int = 3,
) -> List[Tuple[int, int]]:
    frontier: List[Tuple[int, Tuple[int, int], int]] = [(0, start, fuel)]
    visited: Set[Tuple[int, int, int]] = set()
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {start: None}
    g_cost: Dict[Tuple[int, int], int] = {start: 0}

    while frontier:
        _, current, current_fuel = heapq.heappop(frontier)

        if city_map.is_goal_multi_agents(current, goal):
            if level >= 2:
                if g_cost[current] <= city_map.delivery_time:
                    return reconstruct_path(parent, start, goal)
                else:
                    return []
            return reconstruct_path(parent, start, goal)

        if (current, current_fuel) in visited:
            continue

        visited.add((current, current_fuel))

        for direction in DIRECTIONS:
            next_cell = (current[0] + direction[0], current[1] + direction[1])
            if city_map.is_valid_move(next_cell):
                next_fuel = current_fuel - 1
                if next_fuel < 0:
                    continue  # Not enough fuel to move to the next cell

                tentative_g_cost = g_cost[current] + city_map.get_cost(next_cell)
                if city_map.get_cell(next_cell).type == CellType.FUEL_STATION:
                    next_fuel = city_map.fuel_capacity  # Refill fuel

                if next_cell not in g_cost or tentative_g_cost < g_cost[next_cell]:
                    g_cost[next_cell] = tentative_g_cost
                    f_cost = tentative_g_cost + heuristic_2(
                        next_cell, goal, city_map, next_fuel
                    )
                    heapq.heappush(
                        frontier,
                        (f_cost, next_cell, next_fuel),
                    )
                    parent[next_cell] = current

    return reconstruct_path(parent, start, goal)
