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

from search_algorithms import bfs, dfs, ucs, gbfs, a_star
from utils import format_path


def main():
    # Input file format: input{input}_level{level}.txt
    input, level = (4, 1)
    filepath = f"../data/input/input{input}_level{level}.txt"

    pygame.init()
    city_map = CityMap.from_file(filepath)

    # Draw the map screen
    screen_width = city_map.cols * CELL_SIZE
    screen_height = city_map.rows * CELL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Search Algorithm Visualization")

    font = pygame.font.SysFont(None, 24)
    draw_grid(screen, city_map, font)
    pygame.display.update()

    # Run search algorithm
    algorithms = {
        # "BFS": bfs.bfs,
        # "DFS": dfs.dfs,
        # "UCS": ucs.ucs,
        # "GBFS": gbfs.gbfs,
        # "AStar": a_star.astar,
    }

    # Run each algorithm and write the output to a file

    for name, algorithm in algorithms.items():
        path = algorithm(city_map)
        formatted_path = format_path(path)
        output_file = f"../data/output/output{input}_level{level}_{name}.txt"
        with open(output_file, "w") as f:
            f.write(formatted_path)

        # Visualize the path
        visualize_path(screen, path, font)
        pygame.display.update()
        pygame.time.wait(1000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
