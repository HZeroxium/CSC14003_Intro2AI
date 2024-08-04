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
    RED = (255, 0, 0)

    @staticmethod
    def draw_grid(env, agent, screen, font):
        for row in range(env.size):
            for col in range(env.size):
                x = col * GraphicsManager.CELL_SIZE
                y = row * GraphicsManager.CELL_SIZE
                rect = pygame.Rect(
                    x, y, GraphicsManager.CELL_SIZE, GraphicsManager.CELL_SIZE
                )

                cell_color = (
                    GraphicsManager.BACKGROUND_COLOR
                    if (row, col) in agent.visited
                    else GraphicsManager.GRAY
                )
                pygame.draw.rect(screen, cell_color, rect)

                if any(
                    (elem, row, col) in agent.dangerous_cells
                    for elem in [Element.PIT, Element.WUMPUS, Element.POISONOUS_GAS]
                ):
                    pygame.draw.rect(screen, GraphicsManager.RED, rect)
                    text_surface = font.render(
                        env.cell_to_string(env.map[row][col]),
                        True,
                        GraphicsManager.TEXT_COLOR,
                    )
                    screen.blit(text_surface, (x + 5, y + 5))

                pygame.draw.rect(screen, GraphicsManager.GRID_COLOR, rect, 1)

                if (row, col) in agent.visited:
                    text_surface = font.render(
                        env.cell_to_string(env.map[row][col]),
                        True,
                        GraphicsManager.TEXT_COLOR,
                    )
                    screen.blit(text_surface, (x + 5, y + 5))

                if (row, col) == agent.position:
                    pygame.draw.rect(screen, GraphicsManager.RED, rect, 3)

    @staticmethod
    def draw_info_panel(agent, screen, font, env):
        info_texts = [
            f"Score: {agent.get_score()}",
            f"Health: {agent.health}",
            f"Percepts: {agent.get_percept_string()}",
            f"Actions: {agent.get_action_string()}",
            f"Agent Position: {agent.position}",
            f"Agent Direction: {agent.current_direction}",
            f"Elements: {env.get_element(agent.position)}",
            f"Dangerous Cells: {agent.get_dangerous_cells_str()}",
        ]

        for i, text in enumerate(info_texts):
            surface = font.render(text, True, GraphicsManager.TEXT_COLOR)
            screen.blit(
                surface, (10, env.size * GraphicsManager.CELL_SIZE + 10 + 30 * i)
            )

    @staticmethod
    def draw_button(screen, text, pos, size, color=None):
        color = color or GraphicsManager.GRAY
        font = pygame.font.SysFont(None, 36)
        rect = pygame.Rect(pos, size)

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, GraphicsManager.BLACK, rect, 2)
        text_surface = font.render(text, True, GraphicsManager.BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        return rect
