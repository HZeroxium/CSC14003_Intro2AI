# main.py
from agent import Agent
from environment import Environment
import pygame  # type: ignore

# Constants for screen dimensions and colors
CELL_SIZE = 100
INFO_PANEL_HEIGHT = 200
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800 + INFO_PANEL_HEIGHT
FONT_SIZE = 24
BACKGROUND_COLOR = (255, 255, 255)
GRID_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (0, 255, 0)
BUTTON_HOVER_COLOR = (50, 205, 50)
BUTTON_TEXT_COLOR = (0, 0, 0)
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)


def draw_grid(env: Environment, agent: Agent, screen, font):
    for row in range(env.size):
        for col in range(env.size):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)

            # Draw elements in the cell
            elements = env.get_element((row, col))
            text_surface = font.render(
                env.cell_to_string(env.map[row][col]), True, TEXT_COLOR
            )
            screen.blit(text_surface, (x + 5, y + 5))

            # Highlight the agent's current position
            if (row, col) == agent.position:
                pygame.draw.rect(screen, (255, 0, 0), rect, 3)


def draw_info_panel(agent, screen, font, env):
    score_text = f"Score: {agent.get_score()}"
    health_text = f"Health: {agent.health}"
    percept_text = f"Percepts: {agent.get_percept_string()}"
    action_text = f"Actions: {agent.get_action_string()}"
    agent_position = f"Agent Position: {agent.position}"
    agent_direction = f"Agent Direction: {agent.current_direction}"

    score_surface = font.render(score_text, True, TEXT_COLOR)
    health_surface = font.render(health_text, True, TEXT_COLOR)
    percept_surface = font.render(percept_text, True, TEXT_COLOR)
    action_surface = font.render(action_text, True, TEXT_COLOR)
    position_surface = font.render(agent_position, True, TEXT_COLOR)
    agent_direction_surface = font.render(agent_direction, True, TEXT_COLOR)

    screen.blit(score_surface, (10, env.size * CELL_SIZE + 10))
    screen.blit(health_surface, (10, env.size * CELL_SIZE + 40))
    screen.blit(percept_surface, (10, env.size * CELL_SIZE + 70))
    screen.blit(action_surface, (10, env.size * CELL_SIZE + 100))
    screen.blit(position_surface, (10, env.size * CELL_SIZE + 130))
    screen.blit(agent_direction_surface, (10, env.size * CELL_SIZE + 160))


# Function to draw a button on the screen
def draw_button(screen, text, pos, size, color=GRAY):
    font = pygame.font.SysFont(None, 36)
    rect = pygame.Rect(pos, size)

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    return rect


def main():
    env = Environment("../data/input/map1.txt")
    agent = Agent(
        initial_position=env.get_agent_position(), grid_size=env.get_map_size()
    )

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Wumpus World")
    font = pygame.font.SysFont(None, FONT_SIZE)

    running = True
    next_step = False
    next_step_button = draw_button(
        screen=screen,
        text="Next",
        size=(BUTTON_WIDTH, BUTTON_HEIGHT),
        pos=(SCREEN_WIDTH - BUTTON_WIDTH - 10, SCREEN_HEIGHT - INFO_PANEL_HEIGHT + 10),
    )
    pygame.display.update()
    while running and not agent.is_game_over():
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
        elements = env.get_element(agent.position)
        actions = agent.choose_action(percepts, elements)
        new_elements = env.update(agent, actions)
        agent.update_knowledge(new_elements)
        next_step = False

        screen.fill(BACKGROUND_COLOR)
        draw_grid(env, agent, screen, font)
        draw_info_panel(agent, screen, font, env=env)

        pygame.display.flip()

        next_step = False
        next_step_button = draw_button(
            screen=screen,
            text="Next",
            size=(BUTTON_WIDTH, BUTTON_HEIGHT),
            pos=(
                SCREEN_WIDTH - BUTTON_WIDTH - 10,
                SCREEN_HEIGHT - INFO_PANEL_HEIGHT + 10,
            ),
        )
        pygame.display.update()

    print(f"Final Score: {agent.get_score()}")


if __name__ == "__main__":
    main()
