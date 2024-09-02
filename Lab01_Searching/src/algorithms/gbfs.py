import heapq
from utils.graph import Graph
from utils.input_output import map_func, convert_to_char_list


def search(graph: Graph, start: int, goal: int) -> list:
    queue = [
        (graph.get_heuristic(start), start, [])
    ]  # Initialize queue with start node
    visited = set()  # Initialize visited set

    while queue:
        # print("* Queue:", list(map(lambda x: map_func(x[1]), queue)))
        _, node, path = heapq.heappop(queue)
        # print("==> Pop node", map_func(node), "from queue")

        if node in visited:
            continue
        path = path + [node]

        # print("Current path:", list(map(map_func, path)))

        if graph.is_goal(node, goal):
            return path
        visited.add(node)

        # Early stopping if the goal is found
        neighbors = graph.get_neighbors(node)
        # print("Neighbors of", map_func(node), ":", convert_to_char_list(neighbors))
        if goal in neighbors:
            return path + [goal]

        # Expand the node and add neighbors to the queue
        for neighbor in neighbors:
            weight = graph.get_weight(node, neighbor)
            if neighbor not in visited and weight > 0:
                # print(
                #     "Add node",
                #     map_func(neighbor),
                #     "to queue with path",
                #     list(map(map_func, path + [neighbor])),
                # )
                # Remove node neighbor from queue if it is already in the queue
                queue = [(f, n, p) for f, n, p in queue if n != neighbor]
                heapq.heappush(queue, (graph.get_heuristic(neighbor), neighbor, path))

    return -1
