import heapq
from utils.graph import Graph


def search(graph: Graph, start: int, goal: int) -> list:
    queue = [
        (graph.get_heuristic(start), 0, start, [])
    ]  # Initialize queue with start node

    visited = set()  # Initialize visited set
    while queue:
        _, cost, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        path = path + [node]
        if graph.is_goal(node, goal):
            return path
        visited.add(node)
        for neighbor in graph.get_neighbors(node):
            weight = graph.get_weight(node, neighbor)
            if neighbor not in visited and weight > 0:
                heapq.heappush(
                    queue,
                    (
                        cost + weight + graph.get_heuristic(neighbor),
                        cost + weight,
                        neighbor,
                        path,
                    ),
                )

    return -1
