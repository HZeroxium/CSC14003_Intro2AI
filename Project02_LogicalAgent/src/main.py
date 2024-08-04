import pygame  # type: ignore
from agent import Agent
from environment import Environment
from graphics_manager import GraphicsManager


def main():
    env = Environment("../data/input/map1.txt")
    agent = Agent(
        initial_position=env.get_agent_position(), grid_size=env.get_map_size()
    )

    GraphicsManager.set_dimensions(env.get_map_size())

    pygame.init()
    screen = pygame.display.set_mode(
        (GraphicsManager.SCREEN_WIDTH, GraphicsManager.SCREEN_HEIGHT)
    )
    pygame.display.set_caption("Wumpus World")
    font = pygame.font.SysFont(None, GraphicsManager.FONT_SIZE)

    running = True
    next_step = False

    screen.fill(GraphicsManager.BACKGROUND_COLOR)
    next_step_button = GraphicsManager.draw_centered_button(
        screen=screen,
        text="Play",
        size=(GraphicsManager.BUTTON_WIDTH, GraphicsManager.BUTTON_HEIGHT),
        color=GraphicsManager.GREEN,
    )
    pygame.display.update()

    step = 0

    while running and not (agent.is_game_over() or agent.is_game_won()):
        while not next_step:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and next_step_button.collidepoint(event.pos)
                ):
                    next_step = True

        if not running:
            break

        step += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        percepts = env.get_percept(agent.position)
        element = env.get_element(agent.position)
        actions = agent.choose_action(percepts, element)

        screen.fill(GraphicsManager.BACKGROUND_COLOR)
        GraphicsManager.draw_grid(env, agent, screen, font)
        GraphicsManager.draw_info_panel(agent, screen, font, env)

        next_step_button = GraphicsManager.draw_button(
            screen=screen,
            text="Next Step",
            size=(GraphicsManager.BUTTON_WIDTH, GraphicsManager.BUTTON_HEIGHT),
            pos=(
                GraphicsManager.SCREEN_WIDTH - GraphicsManager.BUTTON_WIDTH - 10,
                GraphicsManager.SCREEN_HEIGHT - GraphicsManager.BUTTON_HEIGHT - 10,
            ),
            color=GraphicsManager.YELLOW,
        )
        pygame.display.update()

        new_percept = env.update(agent, actions)
        agent.update_knowledge(new_percept)

        next_step = False

    print(f"Final Score: {agent.get_score()}")

    final_message = "You won!" if agent.is_game_won() else "You lost!"

    screen.fill(GraphicsManager.BACKGROUND_COLOR)
    GraphicsManager.draw_text(
        screen,
        final_message,
        pygame.Rect(
            0,
            0,
            GraphicsManager.SCREEN_WIDTH,
            GraphicsManager.SCREEN_HEIGHT - 3 * GraphicsManager.BUTTON_HEIGHT,
        ),
        font=pygame.font.SysFont(None, 72),
    )

    exit_color = GraphicsManager.GREEN if agent.is_game_won() else GraphicsManager.RED

    exit_button = GraphicsManager.draw_centered_button(
        screen=screen,
        text="Exit",
        size=(GraphicsManager.BUTTON_WIDTH, GraphicsManager.BUTTON_HEIGHT),
        color=exit_color,
    )
    pygame.display.update()
    # Wait for the user click the exit button
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN and exit_button.collidepoint(
                event.pos
            ):
                running = False

    pygame.display.update()


if __name__ == "__main__":
    main()
