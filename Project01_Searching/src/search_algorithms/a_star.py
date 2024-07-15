from citymap import CityMap, CellType
from utils import reconstruct_path, DIRECTIONS, heuristic
import heapq
from typing import Dict, Set, List, Tuple


def a_star(
    city_map: CityMap,
    start: Tuple[int, int] = None,
    goal: Tuple[int, int] = None,
    level: int = 1,
    multi_agent: bool = False,
) -> List[Tuple[int, int]]:
    if start is None:
        start = city_map.start
    if goal is None:
        goal = city_map.goal

    frontier: List[Tuple[int, Tuple[int, int], int]] = [
        (0, start, city_map.fuel if level >= 3 else 0)
    ]
    visited: Set[Tuple[int, int, int]] = set()
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {start: None}
    g_cost: Dict[Tuple[int, int], int] = {start: 0}

    while frontier:
        _, current, current_fuel = heapq.heappop(frontier)

        if (multi_agent and city_map.is_goal_multi_agents(current, goal)) or (
            not multi_agent and city_map.is_goal(current)
        ):
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
                next_fuel = current_fuel - 1 if level >= 3 else current_fuel
                if next_fuel < 0:
                    continue  # Not enough fuel to move to the next cell

                tentative_g_cost = g_cost[current] + city_map.get_cost(next_cell)
                if (
                    city_map.get_cell(next_cell).type == CellType.FUEL_STATION
                    and level >= 3
                ):
                    next_fuel = city_map.fuel_capacity  # Refill fuel

                if next_cell not in g_cost or tentative_g_cost < g_cost[next_cell]:
                    g_cost[next_cell] = tentative_g_cost
                    f_cost = tentative_g_cost + heuristic(
                        next_cell, goal, city_map, level, next_fuel
                    )
                    heapq.heappush(
                        frontier,
                        (f_cost, next_cell, next_fuel),
                    )
                    parent[next_cell] = current

    return []


# Now, you can use this generalized A* function for different levels:
# For Level 1: a_star_general(city_map, level=1)
# For Level 2: a_star_general(city_map, level=2)
# For Level 3: a_star_general(city_map, level=3)
# For multi-agent (Level 4): a_star_general(city_map, level=4, multi_agent=True, start=agent_start, goal=agent_goal)
