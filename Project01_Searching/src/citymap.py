"""
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

# Define enum for cell types

from enum import Enum
from typing import List, Tuple, Optional


class CellType(Enum):
    EMPTY = 0
    START = 1
    GOAL = 2
    FUEL_STATION = 3
    TOLL_ROAD = 4
    OBSTACLE = 5

    def __str__(self):
        if self == CellType.START:
            return "S"
        elif self == CellType.GOAL:
            return "G"
        elif self == CellType.FUEL_STATION:
            return "F"
        return ""


# Define class for cell


class Cell:
    def __init__(
        self,
        row: int,
        col: int,
        type: CellType,
        value: int = 1,
        parent: Optional["Cell"] = None,
    ):
        self.row = row
        self.col = col
        self.type = type
        self.value = value
        self.parent = parent

    def __str__(self):
        return f"{self.type}{self.value}({self.row}, {self.col})"


class CityMap:
    def __init__(
        self,
        rows: int,
        cols: int,
        delivery_time: int,
        fuel_capacity: int,
        grid: List[List["Cell"]],
        start: Tuple[int, int],
        goal: Tuple[int, int],
    ):
        self.rows = rows
        self.cols = cols
        self.delivery_time = delivery_time
        self.fuel_capacity = fuel_capacity
        self.grid = grid
        self.start = start
        self.goal = goal

    @staticmethod
    def from_file(filepath: str) -> "CityMap":
        with open(filepath, "r") as file:
            lines = file.readlines()
            rows, cols, delivery_time, fuel_capacity = map(
                int, lines[0].strip().split()
            )
            temp_grid = [list(map(str, line.strip().split())) for line in lines[1:]]
            start: Tuple[int, int] = None
            goal: Tuple[int, int] = None
            grid = []
            for i in range(rows):
                row = []
                for j in range(cols):
                    cell_type = CellType.EMPTY
                    cell_value = 0
                    if temp_grid[i][j].startswith("S"):
                        cell_type = CellType.START
                        if temp_grid[i][j] == "S":
                            start = (i, j)
                        else:
                            cell_value = int(temp_grid[i][j][1:])
                    elif temp_grid[i][j].startswith("G"):
                        cell_type = CellType.GOAL
                        if temp_grid[i][j] == "G":
                            goal = (i, j)
                        else:
                            cell_value = int(temp_grid[i][j][1:])
                    elif temp_grid[i][j].startswith("F"):
                        # Format: F{value}: F12, F4, ...
                        cell_type = CellType.FUEL_STATION
                        cell_value = int(temp_grid[i][j][1:])
                    elif temp_grid[i][j] == "-1":
                        cell_type = CellType.OBSTACLE
                        cell_value = -1
                    elif temp_grid[i][j] == "0":
                        cell_type = CellType.EMPTY
                    else:
                        cell_type = CellType.TOLL_ROAD
                        cell_value = int(temp_grid[i][j])
                    row.append(Cell(i, j, cell_type, cell_value))
                grid.append(row)
            # print(grid)
            return CityMap(rows, cols, delivery_time, fuel_capacity, grid, start, goal)

    def get_cell(self, position: Tuple[int, int]) -> Cell:
        row, col = position
        return self.grid[row][col]

    def is_valid_move(self, position: Tuple[int, int]) -> bool:
        cell = self.get_cell(position)

        return (
            0 <= position[0] < self.rows
            and 0 <= position[1] < self.cols
            and cell.type != CellType.OBSTACLE
        )

    def is_goal(self, position: Tuple[int, int]) -> bool:
        return position == (self.goal.row, self.goal.col)

    def __str__(self) -> str:
        return f"CityMap({self.rows}, {self.cols}, {self.delivery_time}, {self.fuel_capacity}, {self.start}, {self.goal}, {self.grid})"
