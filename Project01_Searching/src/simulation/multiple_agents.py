from citymap import CityMap, Cell, CellType
from typing import Dict, List, Tuple
from search_algorithms.a_star import a_star
import heapq
from utils import DIRECTIONS, heuristic


class Agent:
    def __init__(self, id: int, start: Tuple[int, int], goal: Tuple[int, int]):
        self.id = id
        self.start = start
        self.goal = goal
        self.path = []

    def __str__(self):
        return f"Agent: {self.start} -> {self.goal}"

    def __eq__(self, other):
        return (
            isinstance(other, Agent)
            and self.id == other.id
            and self.start == other.start
            and self.goal == other.goal
        )


    def __hash__(self):
        return hash((self.id, self.start, self.goal))

def get_agents(city_map: CityMap) -> List[Agent]:
    agents = []
    for i in range(len(city_map.start_points)):
        start = city_map.start_points[i]
        goal = city_map.goal_points[i]

        agents.append(Agent(i, start, goal))
    return agents


def simple_a_star_multi_agent(
    city_map: CityMap, agents: List[Agent]
) -> Dict[Agent, List[Tuple[int, int]]]:
    paths: Dict[Agent, List[Tuple[int, int]]] = {agent: [] for agent in agents}

    for agent in agents:
        path = a_star(
            city_map, level=3, multi_agent=True, start=agent.start, goal=agent.goal
        )
        paths[agent] = path

    return paths


def joint_heuristic(
    positions: List[Tuple[int, int]], goals: List[Tuple[int, int]], city_map: CityMap
) -> int:
    return sum(heuristic(pos, goal, city_map) for pos, goal in zip(positions, goals))


def reconstruct_joint_path(
    parents: Dict[Tuple, Tuple], current: Tuple, city_map: CityMap
) -> Dict[int, List[Tuple[int, int]]]:
    path = {}
    while current in parents:
        prev = parents[current]
        for i, (cur_pos, prev_pos) in enumerate(zip(current, prev)):
            if i not in path:
                path[i] = []
            path[i].append(cur_pos)
        current = prev
    for i in path:
        # Append start position to the path
        path[i].append(city_map.start_points[i])
        path[i].reverse()
    return path


def complex_a_star_multi_agent(
    city_map: CityMap, agents: List[Agent]
) -> Dict[Agent, List[Tuple[int, int]]]:
    start_positions = [agent.start for agent in agents]
    goal_positions = [agent.goal for agent in agents]
    initial_fuel = [city_map.fuel_capacity for i in range(len(agents))]

    open_set = [(0, tuple(start_positions), tuple(initial_fuel))]
    g_cost = {tuple(start_positions): 0}
    f_cost = {
        tuple(start_positions): joint_heuristic(
            start_positions, goal_positions, city_map
        )
    }
    parents = {}
    visited = set()

    while open_set:
        _, current_positions, current_fuel = heapq.heappop(open_set)

        if current_positions in visited:
            continue

        visited.add(current_positions)

        if current_positions == tuple(goal_positions):
            return reconstruct_joint_path(parents, current_positions, city_map=city_map)

        for agent_index, current_pos in enumerate(current_positions):
            if current_fuel[agent_index] <= 0:
                continue

            for direction in DIRECTIONS:
                next_pos = (
                    current_pos[0] + direction[0],
                    current_pos[1] + direction[1],
                )

                if not city_map.is_valid_move(next_pos):
                    continue

                next_positions = list(current_positions)
                next_positions[agent_index] = next_pos
                next_positions = tuple(next_positions)

                next_fuel = list(current_fuel)
                next_fuel[agent_index] -= 1

                if city_map.get_cell(next_pos).type == CellType.FUEL_STATION:
                    next_fuel[agent_index] = city_map.fuel_capacity

                tentative_g_cost = g_cost[current_positions] + city_map.get_cost(
                    next_pos
                )

                if (
                    next_positions not in g_cost
                    or tentative_g_cost < g_cost[next_positions]
                ):
                    g_cost[next_positions] = tentative_g_cost
                    f_cost[next_positions] = tentative_g_cost + joint_heuristic(
                        next_positions, goal_positions, city_map
                    )
                    heapq.heappush(
                        open_set,
                        (f_cost[next_positions], next_positions, tuple(next_fuel)),
                    )
                    parents[next_positions] = current_positions

    return {}
