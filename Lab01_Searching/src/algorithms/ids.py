from utils.graph import Graph


def search(graph: Graph, start: int, goal: int) -> list:
    def dls(node, goal, depth):
        if depth == 0 and graph.is_goal(node, goal):
            return [node]
        if depth > 0:
            for neighbor in graph.get_neighbors(node):
                if graph.get_weight(node, neighbor) > 0:
                    path = dls(neighbor, goal, depth - 1)
                    if path:
                        return [node] + path

        return None

    depth = 0
    while True:
        result = dls(start, goal, depth)
        if result:
            return result
        depth += 1

    return -1
