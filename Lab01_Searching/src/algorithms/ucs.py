import heapq
from utils.graph import Graph


def search(graph: Graph, start: int, goal: int) -> list:
    queue = [(0, start, [])]  # Initialize queue with start node
    visited = set()  # Initialize visited set

    while queue:
        cost, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        path = path + [node]
        if graph.is_goal(node, goal):
            return path
        visited.add(node)
        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                weight = graph.get_weight(node, neighbor)
                heapq.heappush(queue, (cost + weight, neighbor, path))

    return -1


