import pygame  # type: ignore
from utilities import Element


class GraphicsManager:
    MIN_CELL_SIZE = 50
    MAX_CELL_SIZE = 100
    INFO_PANEL_WIDTH = 500
    FONT_SIZE = 24
    BACKGROUND_COLOR = (255, 255, 255)
    GRID_COLOR = (0, 0, 0)
    TEXT_COLOR = (0, 0, 0)
    BUTTON_COLOR = (0, 255, 0)
    BUTTON_HOVER_COLOR = (50, 205, 50)
    BUTTON_TEXT_COLOR = (0, 0, 0)
    BUTTON_WIDTH = 150
    BUTTON_HEIGHT = 50
    BLACK = (0, 0, 0)
    GRAY = (192, 192, 192)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    @classmethod
    def set_dimensions(cls, grid_size):
        cls.CELL_SIZE = max(
            cls.MIN_CELL_SIZE, min(cls.MAX_CELL_SIZE, 1000 // grid_size)
        )
        cls.SCREEN_WIDTH = cls.CELL_SIZE * grid_size + cls.INFO_PANEL_WIDTH
        cls.SCREEN_HEIGHT = cls.CELL_SIZE * grid_size
        cls.FONT_SIZE = cls.CELL_SIZE // 4

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
                    GraphicsManager.draw_text(
                        screen, env.cell_to_string(env.map[row][col]), rect, font
                    )

                pygame.draw.rect(screen, GraphicsManager.GRID_COLOR, rect, 1)

                if (row, col) in agent.visited:
                    GraphicsManager.draw_text(
                        screen, env.cell_to_string(env.map[row][col]), rect, font
                    )

                if (row, col) == agent.position:
                    pygame.draw.rect(screen, GraphicsManager.RED, rect, 3)

    @staticmethod
    def draw_text(screen, text, rect, font):
        text_surface = font.render(text, True, GraphicsManager.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
    
    @staticmethod
    def draw_info_panel(agent, screen, font, env, current_position, previous_position, step_history):
        info_texts = [
            f"Score: {agent.get_score()}",
            f"Health: {agent.health}",
            f"Percepts: {agent.get_percept_string()}",
            f"Actions: {agent.get_action_string()}",
            f"Agent Position: {current_position}",
            f"Agent Direction: {agent.current_direction.name}",
            f"Gold Grabbed: {len(agent.grabbed_gold)}",
            f"Healing Potions: {agent.healing_potions}",
            f"Previous Position: {previous_position}",
        ]

        # Combine info texts with step history, displaying history in reverse order
        display_texts = info_texts + step_history[::-1]

        for i, text in enumerate(display_texts):
            surface = font.render(text, True, GraphicsManager.TEXT_COLOR)
            screen.blit(
                surface, (env.size * GraphicsManager.CELL_SIZE + 10, 10 + 30 * i)
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

    @staticmethod
    def draw_centered_button(screen, text, size, color=None):
        color = color or GraphicsManager.GRAY
        font = pygame.font.SysFont(None, 36)
        rect = pygame.Rect(
            (GraphicsManager.SCREEN_WIDTH - size[0]) // 2,
            (GraphicsManager.SCREEN_HEIGHT - size[1]) // 2,
            *size,
        )

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, GraphicsManager.BLACK, rect, 2)
        text_surface = font.render(text, True, GraphicsManager.BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        return rect
