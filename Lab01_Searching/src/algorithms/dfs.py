from utils.graph import Graph
from collections import deque
from utils.input_output import convert_to_char_list, map_func
from algorithms.bfs import construct_path

# Implement depth-first search algorithm


def search(graph: Graph, start: int, goal: int) -> list:
    # Define helper function to perform DFS
    def dfs(graph: Graph, start: int, goal: int, visited: list, path: list):
        # Mark the current node as visited
        visited[start] = True
        # Append the current node to the path
        path.append(start)

        neighbors = graph.get_neighbors(start)
        if goal in neighbors:
            path.append(goal)
            return True

        # Recur for all the neighbors of the current node
        for neighbor in neighbors:
            if not visited[neighbor]:
                if dfs(graph, neighbor, goal, visited, path):
                    return True

        # If no path is found, backtrack
        path.pop()
        return False

    # Initialize visited list and path
    visited = [False] * graph.nodes
    path = []

    # Perform DFS
    dfs(graph, start, goal, visited, path)

    return path if path else -1
