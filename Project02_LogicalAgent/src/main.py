# main.py
from agent import Agent
from environment import Environment


def main():
    # Initialize the environment
    env = Environment("map1.txt")
    agent = Agent(
        initial_position=env.get_agent_position(), grid_size=env.get_map_size()
    )

    # Main loop
    while not agent.is_game_over():
        percepts = env.get_percept(agent.position)
        actions = agent.choose_action(percepts)
        env.update(agent, actions)
        agent.update_knowledge(percepts)
        # agent.log_action(action)

    print(f"Final Score: {agent.get_score()}")


if __name__ == "__main__":
    main()
