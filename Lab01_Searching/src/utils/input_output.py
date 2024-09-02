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


def map_func(x):
    # if x == 0:
    #     return "S"
    # if x == 1:
    #     return "A"
    # if x == 2:
    #     return "B"
    # if x == 3:
    #     return "C"
    # if x == 4:
    #     return "D"
    # if x == 5:
    #     return "E"
    # if x == 6:
    #     return "F"
    # if x == 7:
    #     return "G"

    # convert x to ASCII character
    return chr(x + 65)


def convert_to_char_list(int_list):
    return list(map(map_func, int_list))


def read_input(file_path: str):
    with open(file_path, "r") as file:
        lines = file.readlines()

    nodes = int(lines[0].strip())
    start, goal = map(int, lines[1].strip().split())
    adjacency_matrix = [
        list(map(int, line.strip().split())) for line in lines[2 : 2 + nodes]
    ]
    heuristic_weights = list(map(int, lines[-1].strip().split()))

    return nodes, start, goal, adjacency_matrix, heuristic_weights


def write_output(file_path: str, results):
    with open(file_path, "w") as file:
        for algorithm, result in results.items():
            file.write(f"{algorithm}:\n")
            file.write(
                f"Path: {' -> '.join(map(str, result['path'])) if result['path'] != -1 else '-1'}\n"
            )
            file.write(f"Time: {result['time']} seconds\n")
            file.write(f"Memory: {result['memory']} KB\n")
            file.write("\n")
