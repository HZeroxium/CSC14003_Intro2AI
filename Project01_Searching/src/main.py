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

import sys
from citymap import CityMap
from simulation.visualizer import draw_grid, visualize_path, CELL_SIZE
import pygame  # type: ignore


def main():
    pygame.init()
    filepath = "../data/input/input5_level4.txt"  # Change this to your input file
    city_map = CityMap.from_file(filepath)
    print()
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
