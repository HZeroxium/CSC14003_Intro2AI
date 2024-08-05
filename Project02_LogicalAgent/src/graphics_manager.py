import pygame  # type: ignore
from utilities import Element


class GraphicsManager:
    # Constants for grid and cell configuration
    MIN_CELL_SIZE = 50
    MAX_CELL_SIZE = 100
    INFO_PANEL_WIDTH = 700
    SCREEN_CALC_DIVISOR = 1000  # Divisor to calculate cell size
    FONT_SIZE_DIVISOR = 4  # Divisor to calculate font size from cell size

    # Font sizes
    SMALL_FONT_SIZE = 14
    BASE_FONT_SIZE = 24
    BUTTON_FONT_SIZE = 36
    TEXT_LINE_SPACING = 30
    TEXT_MARGIN_X = 10
    TEXT_MARGIN_Y = 10

    # Colors for various elements
    BACKGROUND_COLOR = (255, 255, 255)
    GRID_COLOR = (0, 0, 0)
    TEXT_COLOR = (0, 0, 0)
    BUTTON_COLOR = (0, 255, 0)
    BUTTON_HOVER_COLOR = (50, 205, 50)
    BUTTON_TEXT_COLOR = (0, 0, 0)
    BLACK = (0, 0, 0)
    GRAY = (192, 192, 192)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    # Button dimensions
    BUTTON_WIDTH = 150
    BUTTON_HEIGHT = 50
    BUTTON_BORDER_THICKNESS = 2

    # Grid and agent visualization
    GRID_LINE_THICKNESS = 1
    AGENT_HIGHLIGHT_THICKNESS = 3

    @classmethod
    def set_dimensions(cls, grid_size):
        """
        Calculate and set the cell size and screen dimensions based on the grid size.
        """
        # Calculate cell size to be within the min and max limits
        cls.CELL_SIZE = max(
            cls.MIN_CELL_SIZE,
            min(cls.MAX_CELL_SIZE, cls.SCREEN_CALC_DIVISOR // grid_size),
        )
        # Calculate screen width and height
        cls.SCREEN_WIDTH = cls.CELL_SIZE * grid_size + cls.INFO_PANEL_WIDTH
        cls.SCREEN_HEIGHT = cls.CELL_SIZE * grid_size
        cls.FONT_SIZE = cls.CELL_SIZE // cls.FONT_SIZE_DIVISOR

    @staticmethod
    def draw_grid(env, agent, screen, font):
        """
        Draw the grid, highlighting visited and dangerous cells, and the agent's position.
        """
        for row_index in range(env.size):
            for col_index in range(env.size):
                # Calculate position of the cell
                x_position = col_index * GraphicsManager.CELL_SIZE
                y_position = row_index * GraphicsManager.CELL_SIZE
                rect = pygame.Rect(
                    x_position,
                    y_position,
                    GraphicsManager.CELL_SIZE,
                    GraphicsManager.CELL_SIZE,
                )

                # Determine cell color based on visited status
                cell_color = (
                    GraphicsManager.BACKGROUND_COLOR
                    if (row_index, col_index) in agent.visited
                    else GraphicsManager.GRAY
                )
                pygame.draw.rect(screen, cell_color, rect)

                # Highlight dangerous cells
                if any(
                    (elem, row_index, col_index) in agent.dangerous_cells
                    for elem in [Element.PIT, Element.WUMPUS, Element.POISONOUS_GAS]
                ):
                    pygame.draw.rect(screen, GraphicsManager.RED, rect)
                    GraphicsManager.draw_text(
                        screen,
                        env.cell_to_string(env.map[row_index][col_index]),
                        rect,
                        font,
                    )

                # Draw grid lines
                pygame.draw.rect(
                    screen,
                    GraphicsManager.GRID_COLOR,
                    rect,
                    GraphicsManager.GRID_LINE_THICKNESS,
                )

                # Render text for visited cells
                if (row_index, col_index) in agent.visited:
                    GraphicsManager.draw_text(
                        screen,
                        env.cell_to_string(env.map[row_index][col_index]),
                        rect,
                        font,
                    )

                # Highlight agent's current position
                if (row_index, col_index) == agent.position:
                    pygame.draw.rect(
                        screen,
                        GraphicsManager.RED,
                        rect,
                        GraphicsManager.AGENT_HIGHLIGHT_THICKNESS,
                    )

    @staticmethod
    def draw_text(screen, text, rect, font):
        """
        Render text centered within the specified rectangle on the screen.
        """
        text_surface = font.render(text, True, GraphicsManager.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    @staticmethod
    def draw_info_panel(
        agent, screen, font, env, current_position, previous_position, step_history
    ):
        """
        Display the information panel showing agent stats and step history using a smaller monospace font.
        """
        # Use a smaller monospace font for consistent character width
        monospace_font = pygame.font.SysFont(
            "Courier New", GraphicsManager.SMALL_FONT_SIZE
        )

        # List of informational text lines
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
            f"Visited Cells: {len(agent.visited)}",
            f"Dangerous Cells: {len(agent.dangerous_cells)}",
        ]

        # Combine info texts with step history, displaying history in reverse order
        display_texts = info_texts + step_history[::-1]

        # Render each line of text using the smaller monospace font
        for index, text in enumerate(display_texts):
            surface = monospace_font.render(text, True, GraphicsManager.TEXT_COLOR)
            screen.blit(
                surface,
                (
                    env.size * GraphicsManager.CELL_SIZE
                    + GraphicsManager.TEXT_MARGIN_X,
                    GraphicsManager.TEXT_MARGIN_Y
                    + GraphicsManager.TEXT_LINE_SPACING * index,
                ),
            )

    @staticmethod
    def draw_button(screen, text, pos, size, color=None):
        """
        Draw a button with text at the specified position and size.
        """
        color = color or GraphicsManager.GRAY
        font = pygame.font.SysFont(None, GraphicsManager.BUTTON_FONT_SIZE)
        rect = pygame.Rect(pos, size)

        # Draw button and border
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(
            screen, GraphicsManager.BLACK, rect, GraphicsManager.BUTTON_BORDER_THICKNESS
        )

        # Render button text
        text_surface = font.render(text, True, GraphicsManager.BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        return rect

    @staticmethod
    def draw_centered_button(screen, text, size, color=None):
        """
        Draw a button centered on the screen with the specified text and size.
        """
        color = color or GraphicsManager.GRAY
        font = pygame.font.SysFont(None, GraphicsManager.BUTTON_FONT_SIZE)
        rect = pygame.Rect(
            (GraphicsManager.SCREEN_WIDTH - size[0]) // 2,
            (GraphicsManager.SCREEN_HEIGHT - size[1]) // 2,
            *size,
        )

        # Draw centered button and border
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(
            screen, GraphicsManager.BLACK, rect, GraphicsManager.BUTTON_BORDER_THICKNESS
        )

        # Render button text
        text_surface = font.render(text, True, GraphicsManager.BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        return rect
