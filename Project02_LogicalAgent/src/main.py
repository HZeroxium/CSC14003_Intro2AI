# main.py

from program import Program
from agent import Agent
from environment import Environment


def main():
    # Initialize the environment
    env = Environment("map1.txt")
    agent = Agent()

    # Main loop
    while not agent.is_game_over():
        percepts = env.get_percept(agent.position)
        action = agent.choose_action(percepts)
        env.update(agent, action)
        agent.update_knowledge(percepts)
        agent.log_action(action)

    print(f"Final Score: {agent.get_score()}")


if __name__ == "__main__":
    main()
