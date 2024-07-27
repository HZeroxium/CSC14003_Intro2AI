# Project01: Searching - Delivery System

## How to run the program

At `src/` directory:

- 1. Run the following command to install the required packages:

```bash
    pip install -r requirements.txt
```

- 2. Run the program with the following command:

```bash
    python main.py
```

- 3. Follow the instructions on the console to select the input file and search algorithm.

## Project Structure

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
│   ├── requirements.txt        # Required packages for the project
│   └── README.md               # Project description and instructions
├── data/                       # Input and output data
│   ├── input/                  # Input data
|   |   ├── input1_level1.txt   # Input data for level 1 of input 1
|   |   ├── input1_level2.txt   # Input data for level 2 of input 1
|   |-- output/                 # Output data
|   |   ├── output1_level1.txt  # Output data for level 1 of input 1
|   |   ├── output1_level2.txt  # Output data for level 2 of input 1
│
|── Report.pdf                  # Report for the project (included video URLs)


```
