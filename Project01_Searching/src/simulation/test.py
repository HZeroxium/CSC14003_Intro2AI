from typing import List, Dict, Tuple
from copy import deepcopy
from citymap import CityMap
from search_algorithms.a_star import a_star
from simulation.multiple_agents import Agent


def cbs_multiple_agent(
    city_map: CityMap, agents: List[Agent]
) -> Dict[Agent, List[Tuple[int, int]]]:
    # Initialize paths for each agent using A* search
    paths = {
        agent: a_star(city_map, agent.start, agent.goal, multi_agent=True)
        for agent in agents
    }

    # Main CBS loop
    max_iterations = 1000
    iteration = 0
    while iteration < max_iterations:
        # Detect conflicts
        conflicts = detect_conflicts(paths)

        if not conflicts:
            break  # No conflicts, solution found

        # Resolve conflicts
        resolve_conflicts(conflicts, paths)

        iteration += 1

    return paths


def detect_conflicts(
    paths: Dict[Agent, List[Tuple[int, int]]]
) -> List[Tuple[Agent, Agent]]:
    conflicts = []

    # Compare each pair of agents
    for agent1 in paths:
        for agent2 in paths:
            if agent1 != agent2:
                for step in range(min(len(paths[agent1]), len(paths[agent2]))):
                    if paths[agent1][step] == paths[agent2][step]:
                        conflicts.append((agent1, agent2))
                        break

    return conflicts


def resolve_conflicts(
    conflicts: List[Tuple[Agent, Agent]], paths: Dict[Agent, List[Tuple[int, int]]]
):
    for agent1, agent2 in conflicts:
        # Insert wait actions or adjust paths to resolve conflicts
        adjust_paths(agent1, agent2, paths)


def adjust_paths(
    agent1: Agent, agent2: Agent, paths: Dict[Agent, List[Tuple[int, int]]]
):
    # Deep copy paths to avoid modifying original paths prematurely
    paths_copy = deepcopy(paths)

    # Find the first conflicting step
    conflict_step = 0
    while (
        conflict_step < len(paths_copy[agent1])
        and conflict_step < len(paths_copy[agent2])
        and paths_copy[agent1][conflict_step] != paths_copy[agent2][conflict_step]
    ):
        conflict_step += 1

    # Adjust path of agent1
    new_path_agent1 = []
    for step in range(len(paths[agent1])):
        if step < conflict_step:
            new_path_agent1.append(paths[agent1][step])
        else:
            # Insert wait action or alternative path segment
            new_path_agent1.append(
                paths[agent1][step - 1]
            )  # Simulate waiting by repeating previous step

    paths[agent1] = new_path_agent1

    # Check if agent2's path needs adjustment
    if agent2 in paths:
        # Ensure agent2's path is not already adjusted
        if paths[agent2] != paths_copy[agent2]:
            adjust_paths(
                agent2, agent1, paths
            )  # Recursive call to handle symmetrically


# Example usage:
# Assuming `city_map` and `agents` are properly initialized
# city_map = CityMap.from_file("map.txt")
# agents = [Agent(1, city_map.start, city_map.goal), Agent(2, city_map.start_points[1], city_map.goal_points[1])]
# paths = find_multiple_agent_paths(city_map, agents)
# for agent, path in paths.items():
#     print(f"Agent {agent.id} path: {path}")
