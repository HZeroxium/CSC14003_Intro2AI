# You are required to implement and compare various graph search algorithms. The algorithms to
# be included in this lab are as follows:
# 1. Breadth-first search (BFS)
# 2. Tree-search Depth-first search (DFS)
# 3. Uniform-cost search (UCS)
# 4. Iterative deepening search (IDS)
# 5. Greedy best-first search (GBFS)
# 6. Graph-search A* (A*)
# 7. Hill-climbing (HC) variant

# You will:
# • Read input from a file.
# • Perform path search from the start node to the goal node on a given graph.
# • Write the results to an output file.
# • Compare and evaluate the algorithms based on runtime and memory usage.
# Please note that:
# • BFS, DFS and GBFS algorithms stop when the goal node is generated, not when the goal
# node is expanded.
# • UCS and A* algorithms stop when the goal node is expanded.
# • If Hill Climbing algorithm gets stuck, it is considered as having no path.

# The input file contains information about the graph and weights, formatted as follows:
# • The first line contains the number of nodes in the graph.
# • The second line contains two integers representing the start and goal nodes.
# • The subsequent lines contain the adjacency matrix of the graph.
# • The last line contains the heuristic weights for each node (for algorithms that use heuristics).
# Note that the graph can be either directed or undirected.

# Example input file:
# 5
# 0 3
# 0 4 5 0 0
# 4 0 2 5 6
# 5 2 0 3 0
# 0 5 3 0 1
# 0 6 0 1 0
# 8 5 3 0 1 (heuristic weights)

# The output file should contain the following information:
# • The path from the start node to the goal node for each algorithm.
# If there is no path, the output is -1.
# • The runtime and memory usage of each algorithm.
# Example output file:
# BFS:
# Path: 0 -> 1 -> 3
# Time: 0.0000003 seconds
# Memory: 8 KB
# ...
# Hill-climbing:
# Path: 0 -> 2 -> 3
# Time: 0.0000003 seconds
# Memory: 8 KB

# main.py

from utils.graph import Graph
from utils.input_output import read_input, write_output
from utils.performance import measure_performance
from algorithms import bfs, dfs, ucs, ids, gbfs, astar, hc


def main():
    dir_path = "test/test05/"
    input_file = dir_path + "input.txt"
    output_file = dir_path + "output.txt"
    # Read input from file
    nodes, start, goal, adjacency_matrix, heuristic_weights = read_input(input_file)

    # print(nodes, start, goal, adjacency_matrix, heuristic_weights, sep="\n")

    # Create graph object
    graph = Graph(nodes, adjacency_matrix, heuristic_weights)

    # Dictionary to store results
    results = {}

    # List of algorithms to run
    algorithms = {
        "BFS": bfs.search,
        "DFS": dfs.search,
        "UCS": ucs.search,
        "IDS": ids.search,
        "GBFS": gbfs.search,
        "A*": astar.search,
        "Hill-climbing": hc.search,
    }
    # Run each algorithm and measure performance
    for name, algorithm in algorithms.items():
        path, time_taken, memory_used = measure_performance(
            algorithm, graph, start, goal
        )
        results[name] = {"path": path, "time": time_taken, "memory": memory_used}

    # Write results to output file
    write_output(output_file, results)


if __name__ == "__main__":
    main()
