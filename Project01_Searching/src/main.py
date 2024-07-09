"""
Project_DeliverySystem/
│
├── src/                        # Source code directory
│   ├── __init__.py             # Indicates that this directory is a Python package
│   ├── main.py                 # Entry point for the program
│   ├── utils.py                # Utility functions (e.g., file I/O, map parsing)
│   ├── search_algorithms/      # Directory for search algorithm implementations
│   │   ├── __init__.py         # Indicates that this directory is a Python package
│   │   ├── bfs.py              # Breadth-First Search algorithm
│   │   ├── dfs.py              # Depth-First Search algorithm
│   │   ├── ucs.py              # Uniform-Cost Search algorithm
|   |   |── gbfs.py             # Greedy Best-First Search algorithm
│   │   ├── a_star.py           # A* Search algorithm
│   └── simulation/             # Directory for simulation and visualization
│       ├── __init__.py         # Indicates that this directory is a Python package
│       ├── visualizer.py       # Visualization of search process
│       └── multiple_agents.py  # Coordination mechanism for multiple agents
│
├── data/                       # Input and output data
│   ├── input1_level1.txt       # Example input file for Level 1
│   ├── input1_level2.txt       # Example input file for Level 2
│   ├── input1_level3.txt       # Example input file for Level 3
│   ├── input1_level4.txt       # Example input file for Level 4
│   ├── output1_level1.txt      # Example output file for Level 1
│   ├── output1_level2.txt      # Example output file for Level 2
│   ├── output1_level3.txt      # Example output file for Level 3
│   ├── output1_level4.txt      # Example output file for Level 4
│
├── docs/                       # Documentation
│   ├── Report.pdf              # Project report
│   └── README.md               # Project description and instructions
│
├── requirements.txt            # Python dependencies
├── setup.py                    # Setup script for the package
└── tests/                      # Unit tests for the project
    ├── test_bfs.py             # Unit tests for BFS algorithm
    ├── test_dfs.py             # Unit tests for DFS algorithm
    ├── test_ucs.py             # Unit tests for UCS algorithm
    |── test_gbfs.py            # Unit tests for GBFS algorithm
    ├── test_a_star.py          # Unit tests for A* algorithm
    ├── test_simulation.py      # Unit tests for simulation
    └── __init__.py             # Indicates that this directory is a Python package


"""

import pygame
import sys
import time

# Constants
CELL_SIZE = 80
GRID_COLOR = (200, 200, 200)
BACKGROUND_COLOR = (255, 255, 255)
START_COLOR = (0, 255, 0)
GOAL_COLOR = (255, 0, 0)
OBSTACLE_COLOR = (0, 0, 0)
PATH_COLOR = (0, 0, 255)
TEXT_COLOR = (0, 0, 0)
FUEL_STATION_COLOR = (255, 255, 0)
TOLL_ROAD_COLOR = (128, 128, 128)


class CityMap:
    def __init__(self, rows, cols, delivery_time, fuel_capacity, grid):
        self.rows = rows
        self.cols = cols
        self.delivery_time = delivery_time
        self.fuel_capacity = fuel_capacity
        self.grid = grid

    @staticmethod
    def from_file(filepath):
        with open(filepath, "r") as file:
            lines = file.readlines()
            rows, cols, delivery_time, fuel_capacity = map(
                int, lines[0].strip().split()
            )
            grid = [list(map(str, line.strip().split())) for line in lines[1:]]
            return CityMap(rows, cols, delivery_time, fuel_capacity, grid)


def draw_grid(screen, city_map, font):
    for row in range(city_map.rows):
        for col in range(city_map.cols):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            value = city_map.grid[row][col]
            if value == "0":
                color = BACKGROUND_COLOR
            elif value == "-1":
                color = OBSTACLE_COLOR
            elif value == "S" or value.startswith("S"):
                color = START_COLOR
            elif value == "G" or value.startswith("G"):
                color = GOAL_COLOR
            elif value.startswith("F"):
                color = FUEL_STATION_COLOR
            else:
                color = TOLL_ROAD_COLOR
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)
            if value not in ["0", "-1"]:
                text_surface = font.render(value, True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)


def visualize_path(screen, path, font):
    for row, col in path:
        x = col * CELL_SIZE
        y = row * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, PATH_COLOR, rect)
        pygame.draw.rect(screen, GRID_COLOR, rect, 1)
        text_surface = font.render("P", True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        time.sleep(0.1)


def main():
    pygame.init()
    filepath = "../data/input/input5_level2.txt"  # Change this to your input file
    city_map = CityMap.from_file(filepath)

    screen_width = city_map.cols * CELL_SIZE
    screen_height = city_map.rows * CELL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Search Algorithm Visualization")

    font = pygame.font.SysFont(None, 24)
    draw_grid(screen, city_map, font)
    pygame.display.update()

    path = [(1, 1), (2, 1), (3, 1), (4, 1)]  # Example path
    # visualize_path(screen, path, font)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
