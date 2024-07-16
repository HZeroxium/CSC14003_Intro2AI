from citymap import CityMap
from utils import reconstruct_path, DIRECTIONS
from typing import Dict, Set, List, Tuple


def dfs(
    city_map: CityMap, start: Tuple[int, int], goal: Tuple[int, int]
) -> List[Tuple[int, int]]:
    stack: List[Tuple[int, int]] = [start]
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {start: None}
    visited: Set[Tuple[int, int]] = set()
    visited.add(start)

    while stack:
        current: Tuple[int, int] = stack.pop()

        if city_map.is_goal(current):
            return reconstruct_path(parent, start, goal)

        for direction in DIRECTIONS:
            neighbor: Tuple[int, int] = (
                current[0] + direction[0],
                current[1] + direction[1],
            )

            if (
                city_map.is_valid_move(neighbor)
                and neighbor not in parent
                and neighbor not in visited
            ):
                stack.append(neighbor)
                parent[neighbor] = current
                visited.add(neighbor)

    return reconstruct_path(parent, start, goal)
