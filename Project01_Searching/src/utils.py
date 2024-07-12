""" 
This module contains utility functions that are used in the project.

Input file format:
The input file is numbered according to the convention input1_level1.txt, input1_level2.txt,
etc. The input file format is described as follows:
• The first line contains 4 positive integers n m t f, corresponding to the number of rows and
columns of the map, committed delivery time, and fuel tank capacity.
• The following n lines represent the information on the map. Encoding conventions are as in
the description, with all letter characters in uppercase.

Example:

10 10 20 10
0 0 0 0 -1 -1 0 0 0 0
0 S 0 0 0 0 0 -1 0 -1
0 0 -1 -1 -1 S1 0 -1 0 -1
0 0 0 0 -1 0 0 -1 0 0
0 0 -1 -1 -1 0 G2 -1 0 0
1 0 -1 0 0 0 0 0 -1 0
0 0 F1 0 -1 4 -1 8 -1 0
0 0 0 0 -1 0 0 0 G 0
0 -1 -1 -1 -1 S2 0 0 0 0
G1 0 5 0 0 0 0 -1 -1 -1 0

n - number of rows: 10
m - number of columns: 10
t - committed delivery time: 20
f - fuel tank capacity: 10
S - starting point of the vehicle 1 (1, 1)
S1 - starting point of the vehicle 2 (3, 5)
S2 - starting point of the vehicle 3 (9, 5)
G - goal point of the vehicle 1 (8, 8)
G1 - goal point of the vehicle 2 (9, 0)
G2 - goal point of the vehicle 3 (5, 6)
F1 - fuel station (6, 2), with 1 minute to refuel
Numbers (1, 4, 5, 8) - indicate the time required to travel between two points

"""

from typing import List, Dict, Tuple
from citymap import CityMap, CellType

# Constants

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def reconstruct_path(
    parent: Dict[Tuple[int, int], Tuple[int, int]],
    start: Tuple[int, int],
    goal: Tuple[int, int],
    debug: bool = False,
) -> List[Tuple[int, int]]:
    path: List[Tuple[int, int]] = []
    current = goal

    # Check if goal is unreachable
    if current not in parent:
        return []

    while current != start:
        if debug:
            print("Current:", current)
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()

    return path


def heuristic(a: tuple, b: tuple) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Output path example: (1, 1) -> (2, 1) -> (3, 1) -> (4, 1)


def format_path(path: List[Tuple[int, int]]) -> str:
    if not path:
        return "No path found"
    return " -> ".join([f"({x}, {y})" for x, y in path])


def heuristic_2(
    a: Tuple[int, int], b: Tuple[int, int], city_map: CityMap, current_fuel: int
) -> int:
    h = abs(a[0] - b[0]) + abs(a[1] - b[1])

    if current_fuel < h:
        # Penalize paths with low fuel
        min_fuel_station_dist = float("inf")
        for i in range(city_map.rows):
            for j in range(city_map.cols):
                if city_map.get_cell((i, j)).type == CellType.FUEL_STATION:
                    dist_to_fuel_station = abs(a[0] - i) + abs(a[1] - j)
                    min_fuel_station_dist = min(
                        min_fuel_station_dist, dist_to_fuel_station
                    )
        h += min_fuel_station_dist * 2  # Penalize distance to the nearest fuel station

    return h
