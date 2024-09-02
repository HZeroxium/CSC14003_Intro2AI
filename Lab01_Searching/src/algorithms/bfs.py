from utils.graph import Graph
from collections import deque

# from utils.input_output import convert_to_char_list, map_func


def search(graph: Graph, start: int, goal: int) -> list:
    queue = deque([start])  # Initialize queue with start node
    visited = set()  # Initialize visited set
    visited.add(start)
    parent = {start: None}  # Initialize parent dictionary

    while queue:
        # print("Current queue: ", convert_to_char_list(list(queue)))
        node = queue.popleft()
        # print("Pop node: ", map_func(node))
        if graph.is_goal(node, goal):
            return construct_path(parent, start, goal)

        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)
    return -1


def construct_path(parent, start, goal):
    path = []
    current = goal
    while current is not start:
        path.append(current)
        current = parent[current]
    path.append(start)
    return path[::-1]
