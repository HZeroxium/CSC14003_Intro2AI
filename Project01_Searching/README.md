# Project01: Searching - Delivery System

``` less
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
│   ├── input/                  # Input data
|   |   ├── input1_level1.txt   # Input data for level 1 of input 1
|   |   ├── input1_level2.txt   # Input data for level 2 of input 1
|   |-- output/                 # Output data
|   |   ├── output1_level1.txt  # Output data for level 1 of input 1
|   |   ├── output1_level2.txt  # Output data for level 2 of input 1
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

```
