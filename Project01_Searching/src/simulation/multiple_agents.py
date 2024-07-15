from citymap import CityMap
from typing import Dict, List, Tuple
from search_algorithms.a_star import a_star


class Agent:
    def __init__(self, start: Tuple[int, int], goal: Tuple[int, int]):
        self.start = start
        self.goal = goal
        self.current_position = start

    def __str__(self):
        return f"Agent: {self.start} -> {self.goal}"


def get_agents(city_map: CityMap) -> List[Agent]:
    agents = []
    for i in range(len(city_map.start_points)):
        start = city_map.start_points[i]
        goal = city_map.goal_points[i]
        agents.append(Agent(start, goal))
    return agents


def a_star_multi_agent(
    city_map: CityMap, agents: List[Agent]
) -> Dict[Agent, List[Tuple[int, int]]]:
    paths: Dict[Agent, List[Tuple[int, int]]] = {agent: [] for agent in agents}

    for agent in agents:
        path = a_star(
            city_map, level=3, multi_agent=True, start=agent.start, goal=agent.goal
        )
        paths[agent] = path

    return paths


# def a_star_multi_agent_optimized(
#     city_map: CityMap, agents: List[Agent]
# ) -> Dict[Agent, List[Tuple[int, int]]]:
#     block_cells: Dict[int, Dict[int, Set[Tuple[int, int]]]] = {
#         i: {} for i in range(len(agents))
#     }
#     paths: Dict[Agent, List[Tuple[int, int]]] = {agent: [] for agent in agents}
#     open_sets: List[List[Tuple[int, Tuple[int, int], int]]] = [[] for _ in agents]
#     parents: List[Dict[Tuple[int, int], Tuple[int, int]]] = [{} for _ in agents]
#     g_scores: List[Dict[Tuple[int, int], int]] = [{agent.start: 0} for agent in agents]
#     f_scores: List[Dict[Tuple[int, int], int]] = [
#         {agent.start: heuristic_2(agent.start, agent.goal, city_map, agent.fuel)}
#         for agent in agents
#     ]

#     for i, agent in enumerate(agents):
#         heapq.heappush(
#             open_sets[i], (f_scores[i][agent.start], agent.start, agent.fuel)
#         )

#     while any(open_sets):
#         next_positions = []
#         for agent_index, agent in enumerate(agents):
#             if not open_sets[agent_index]:
#                 continue

#             _, current, current_fuel = heapq.heappop(open_sets[agent_index])
#             next_positions.append((agent_index, current, current_fuel))

#         # Ensure no two agents move to the same cell at the same step
#         unique_positions = set()
#         for agent_index, current, current_fuel in next_positions:
#             if city_map.is_goal(current):
#                 path = reconstruct_path(
#                     parents[agent_index],
#                     agents[agent_index].start,
#                     agents[agent_index].goal,
#                 )
#                 paths[agents[agent_index]] = path
#                 for step in range(len(path)):
#                     if step in block_cells[agent_index]:
#                         block_cells[agent_index][step].add(path[step])
#                     else:
#                         block_cells[agent_index][step] = {path[step]}
#                 continue

#             for direction in DIRECTIONS:
#                 next_cell = (current[0] + direction[0], current[1] + direction[1])
#                 if city_map.is_valid_move(next_cell):
#                     next_fuel = current_fuel - 1
#                     if next_fuel < 0:
#                         continue  # Not enough fuel to move to the next cell

#                     tentative_g_score = g_scores[agent_index][
#                         current
#                     ] + city_map.get_cost(next_cell)
#                     if city_map.get_cell(next_cell).type == CellType.FUEL_STATION:
#                         next_fuel = city_map.fuel_capacity

#                     if (
#                         next_cell not in g_scores[agent_index]
#                         or tentative_g_score < g_scores[agent_index][next_cell]
#                     ) and (next_cell not in unique_positions):
#                         g_scores[agent_index][next_cell] = tentative_g_score
#                         f_scores[agent_index][next_cell] = (
#                             tentative_g_score
#                             + heuristic_2(
#                                 next_cell, agents[agent_index].goal, city_map, next_fuel
#                             )
#                         )
#                         heapq.heappush(
#                             open_sets[agent_index],
#                             (f_scores[agent_index][next_cell], next_cell, next_fuel),
#                         )
#                         parents[agent_index][next_cell] = current
#                         unique_positions.add(next_cell)

#         # Mark the path of the current step for all agents
#         for step in range(
#             max(len(block_cells[agent_index]) for agent_index in range(len(agents)))
#         ):
#             blocked_positions = set()
#             for agent_index in range(len(agents)):
#                 if step < len(block_cells[agent_index]):
#                     blocked_positions.update(block_cells[agent_index][step])

#             for agent_index in range(len(agents)):
#                 if step in block_cells[agent_index]:
#                     block_cells[agent_index][step].update(blocked_positions)
#                 else:
#                     block_cells[agent_index][step] = blocked_positions.copy()

#         # Print the content of block_cells at each step for debugging
#         for agent_index in range(len(agents)):
#             print(f"Agent {agent_index} block_cells: {block_cells[agent_index]}")

#     return paths
