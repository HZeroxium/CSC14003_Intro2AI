import pygame  # type: ignore
from utilities import Element


class GraphicsManager:
    CELL_SIZE = 100
    INFO_PANEL_HEIGHT = 300
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000 + INFO_PANEL_HEIGHT
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
    GREEN = (0, 255, 0)

    @staticmethod
    def draw_grid(env, agent, screen, font):
        for row in range(env.size):
            for col in range(env.size):
                x = col * GraphicsManager.CELL_SIZE
                y = row * GraphicsManager.CELL_SIZE
                rect = pygame.Rect(
                    x, y, GraphicsManager.CELL_SIZE, GraphicsManager.CELL_SIZE
                )

                # Draw the cell in gray if not visited, else in white
                if (row, col) in agent.visited:
                    cell_color = GraphicsManager.BACKGROUND_COLOR
                else:
                    cell_color = GraphicsManager.GRAY

                pygame.draw.rect(screen, cell_color, rect)

                # Highlight dangerous cells
                if any(
                    (elem, row, col) in agent.dangerous_cells
                    for elem in [Element.PIT, Element.WUMPUS, Element.POISONOUS_GAS]
                ):
                    pygame.draw.rect(screen, GraphicsManager.GREEN, rect)

                pygame.draw.rect(screen, GraphicsManager.GRID_COLOR, rect, 1)

                # Draw elements in the cell only if visited
                if (row, col) in agent.visited:
                    elements = env.get_element((row, col))
                    text_surface = font.render(
                        env.cell_to_string(env.map[row][col]),
                        True,
                        GraphicsManager.TEXT_COLOR,
                    )
                    screen.blit(text_surface, (x + 5, y + 5))

                # Highlight the agent's current position
                if (row, col) == agent.position:
                    pygame.draw.rect(screen, (255, 0, 0), rect, 3)

    @staticmethod
    def draw_info_panel(agent, screen, font, env, elements=None):
        score_text = f"Score: {agent.get_score()}"
        health_text = f"Health: {agent.health}"
        percept_text = f"Percepts: {agent.get_percept_string()}"
        action_text = f"Actions: {agent.get_action_string()}"
        agent_position = f"Agent Position: {agent.position}"
        agent_direction = f"Agent Direction: {agent.current_direction}"
        elements = f"Elements: {env.get_element(agent.position)}"
        dangerous_cells = f"Dangerous Cells: {agent.get_dangerous_cells_str()}"

        score_surface = font.render(score_text, True, GraphicsManager.TEXT_COLOR)
        health_surface = font.render(health_text, True, GraphicsManager.TEXT_COLOR)
        percept_surface = font.render(percept_text, True, GraphicsManager.TEXT_COLOR)
        action_surface = font.render(action_text, True, GraphicsManager.TEXT_COLOR)
        position_surface = font.render(agent_position, True, GraphicsManager.TEXT_COLOR)
        agent_direction_surface = font.render(
            agent_direction, True, GraphicsManager.TEXT_COLOR
        )
        elements_surface = font.render(str(elements), True, GraphicsManager.TEXT_COLOR)
        dangerous_cells_surface = font.render(
            str(dangerous_cells), True, GraphicsManager.TEXT_COLOR
        )

        screen.blit(score_surface, (10, env.size * GraphicsManager.CELL_SIZE + 10))
        screen.blit(health_surface, (10, env.size * GraphicsManager.CELL_SIZE + 40))
        screen.blit(percept_surface, (10, env.size * GraphicsManager.CELL_SIZE + 70))
        screen.blit(action_surface, (10, env.size * GraphicsManager.CELL_SIZE + 100))
        screen.blit(position_surface, (10, env.size * GraphicsManager.CELL_SIZE + 130))
        screen.blit(
            agent_direction_surface, (10, env.size * GraphicsManager.CELL_SIZE + 160)
        )
        screen.blit(elements_surface, (10, env.size * GraphicsManager.CELL_SIZE + 190))
        screen.blit(
            dangerous_cells_surface, (10, env.size * GraphicsManager.CELL_SIZE + 220)
        )

    @staticmethod
    def draw_button(screen, text, pos, size, color=GRAY):
        font = pygame.font.SysFont(None, 36)
        rect = pygame.Rect(pos, size)

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, GraphicsManager.BLACK, rect, 2)
        text_surface = font.render(text, True, GraphicsManager.BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        return rect
