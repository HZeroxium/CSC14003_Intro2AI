class Graph:
    def __init__(
        self,
        nodes: int,
        adjacency_matrix: list[list],
        heuristic_weights: list,
    ):
        self.nodes = nodes
        self.adjacency_matrix = adjacency_matrix
        self.heuristic_weights = heuristic_weights

    def get_neighbors(self, node: int) -> list:
        neighbors = []
        for idx, weight in enumerate(self.adjacency_matrix[node]):
            if weight > 0:
                neighbors.append(idx)

        return neighbors

    def get_heuristic(self, node: int) -> int:
        return self.heuristic_weights[node]

    def is_goal(self, node: int, goal: int) -> bool:
        return node == goal

    def get_weight(self, u: int, v: int) -> int:
        return self.adjacency_matrix[u][v]
