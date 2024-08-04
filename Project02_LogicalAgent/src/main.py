from agent import Agent
from environment import Environment
import pygame  # type: ignore
from graphics_manager import GraphicsManager


def main():
    env = Environment("../data/input/map5.txt")
    agent = Agent(
        initial_position=env.get_agent_position(), grid_size=env.get_map_size()
    )

    pygame.init()
    screen = pygame.display.set_mode(
        (GraphicsManager.SCREEN_WIDTH, GraphicsManager.SCREEN_HEIGHT)
    )
    pygame.display.set_caption("Wumpus World")
    font = pygame.font.SysFont(None, GraphicsManager.FONT_SIZE)

    running = True
    next_step = False

    screen.fill(GraphicsManager.BACKGROUND_COLOR)
    GraphicsManager.draw_grid(env, agent, screen, font)
    GraphicsManager.draw_info_panel(agent, screen, font, env=env)
    next_step_button = GraphicsManager.draw_button(
        screen=screen,
        text="Next",
        size=(GraphicsManager.BUTTON_WIDTH, GraphicsManager.BUTTON_HEIGHT),
        pos=(
            GraphicsManager.SCREEN_WIDTH - GraphicsManager.BUTTON_WIDTH - 10,
            GraphicsManager.SCREEN_HEIGHT - GraphicsManager.INFO_PANEL_HEIGHT + 10,
        ),
    )
    pygame.display.update()
    step = 0

    while running and not (agent.is_game_over() or agent.is_game_won()):
        print("========================================")
        print(f"Step: {step}")
        print("========================================")
        step += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while not next_step:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if next_step_button.collidepoint(event.pos):
                        next_step = True

        percepts = env.get_percept(agent.position)
        element = env.get_element(agent.position)
        actions = agent.choose_action(percepts, element)
        new_percept = env.update(agent, actions)
        agent.update_knowledge(new_percept)
        next_step = False

        screen.fill(GraphicsManager.BACKGROUND_COLOR)
        GraphicsManager.draw_grid(env, agent, screen, font)
        GraphicsManager.draw_info_panel(agent, screen, font, env=env)

        next_step_button = GraphicsManager.draw_button(
            screen=screen,
            text="Next",
            size=(GraphicsManager.BUTTON_WIDTH, GraphicsManager.BUTTON_HEIGHT),
            pos=(
                GraphicsManager.SCREEN_WIDTH - GraphicsManager.BUTTON_WIDTH - 10,
                GraphicsManager.SCREEN_HEIGHT - GraphicsManager.INFO_PANEL_HEIGHT + 10,
            ),
        )
        pygame.display.update()

    print(f"Final Score: {agent.get_score()}")


if __name__ == "__main__":
    main()
