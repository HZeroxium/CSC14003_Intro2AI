from utils.graph import Graph


def search(graph: Graph, start: int, goal: int) -> list:
    current = start
    path = [current]

    while not graph.is_goal(current, goal):
        neighbors = [
            (neighbor, graph.get_heuristic(neighbor))
            for neighbor in graph.get_neighbors(current)
            if graph.get_weight(current, neighbor) > 0
        ]

        if not neighbors:
            return -1  # No path found

        next_node = min(neighbors, key=lambda x: x[1])[0]

        if graph.get_heuristic(next_node) >= graph.get_heuristic(current):
            return -1  # Hill climbing gets stuck

        current = next_node
        path.append(current)

    return path
