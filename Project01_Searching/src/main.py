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

import os
import sys
from citymap import CityMap
from simulation.visualizer import (
    draw_grid,
    visualize_path,
    CELL_SIZE,
    PATH_COLORS,
    visualize_multi_path,
)
import pygame  # type: ignore

from search_algorithms import bfs, dfs, ucs, gbfs, a_star
from utils import format_path
from simulation.multiple_agents import (
    # a_star_multi_agent,
    Agent,
    get_agents,
    a_star_multi_agent,
)


def single_agent(input: int = 1, level: int = 1):
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
        1: {
            "BFS": bfs.bfs,
            "DFS": dfs.dfs,
            "UCS": ucs.ucs,
            "GBFS": gbfs.gbfs,
            "AStar": a_star.a_star,
        },
        2: {
            "AStar": a_star.a_star,
        },
        3: {
            "AStar": a_star.a_star,
        },
    }

    # Run each algorithm and write the output to a file
    i = 0
    paths = {}
    start = city_map.start
    goal = city_map.goal
    for name, algorithm in algorithms[level].items():
        if level == 1:
            path = algorithm(city_map, start, goal)
        if level <= 3:
            path = algorithm(city_map, start, goal, level)
        # Visualize the path
        visualize_path(screen, city_map, path, PATH_COLORS[i])
        pygame.display.update()
        pygame.time.wait(1000)
        i += 1
        paths[name] = path

    # Write to file
    output = f"../data/output/output{input}_level{level}.txt"

    with open(output, "w") as f:
        for name, path in paths.items():
            f.write(f"{name}: {format_path(path)}\n")
            f.write("Path length: {}\n".format(len(path)))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()


def multiple_agent(input: int = 1):
    filepath = f"../data/input/input{input}_level4.txt"

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

    # Run multi-agent search algorithm
    agents = get_agents(city_map)
    paths = a_star_multi_agent(city_map, agents)

    # Print the paths of each agent
    for agent, path in paths.items():
        print(f"Agent {agent}: {path}")

    # Visualize the paths
    visualize_multi_path(screen, city_map, paths)
    # pygame.display.update()

    # Write to file
    # output = f"../data/output/output{input}_level4.txt"

    # with open(output, "w") as f:
    #     for agent, path in paths.items():
    #         f.write(f"{agent}: {format_path(path)}\n")
    #         f.write("Path length: {}\n".format(len(path)))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()


def main():
    # level: int = int(input("Enter level (1-4): "))
    # input_num: int = int(input("Enter input number (1-5): "))
    level, input_num = 4, 4

    if level >= 1 and level <= 3:
        single_agent(input_num, level)
    else:
        multiple_agent(input_num)


if __name__ == "__main__":
    main()
