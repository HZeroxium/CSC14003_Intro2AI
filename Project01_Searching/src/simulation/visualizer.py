import pygame  # type: ignore
import time
from citymap import CityMap, CellType
from typing import List, Tuple, Dict
from simulation.multiple_agents import Agent

# Constants
CELL_SIZE = 80
GRID_COLOR = (200, 200, 200)
BACKGROUND_COLOR = (255, 255, 255)
START_COLOR = (0, 255, 0)
GOAL_COLOR = (255, 0, 0)
OBSTACLE_COLOR = (0, 0, 0)
PATH_COLOR = (0, 0, 255)
TEXT_COLOR = (0, 0, 0)
FUEL_STATION_COLOR = (255, 255, 0)
TOLL_ROAD_COLOR = (128, 128, 128)
TEST_COLOR = (255, 0, 255)
PATH_COLORS = [
    (0, 128, 255),
    (128, 255, 0),
    (255, 0, 128),
    (255, 255, 128),
    (128, 255, 128),
    (255, 128, 128),
    (128, 128, 255),
    (255, 128, 0),
    (128, 0, 255),
]


CONFLICT_SYMBOL = "X"


def draw_grid(screen, city_map: CityMap, font):
    for row in range(city_map.rows):
        for col in range(city_map.cols):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            celltype = city_map.grid[row][col].type
            if celltype == CellType.EMPTY:
                color = BACKGROUND_COLOR
            elif celltype == CellType.OBSTACLE:
                color = OBSTACLE_COLOR
            elif celltype == CellType.START:
                color = START_COLOR
            elif celltype == CellType.GOAL:
                color = GOAL_COLOR
            elif celltype == CellType.FUEL_STATION:
                color = FUEL_STATION_COLOR
            else:
                color = TOLL_ROAD_COLOR
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)
            if celltype not in [CellType.EMPTY, CellType.OBSTACLE]:
                str_value = str(city_map.grid[row][col].value)
                text_surface = font.render(str_value, True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)


def visualize_path(screen, path, color=PATH_COLOR):
    if not path:
        return
    for i in range(len(path) - 1):
        row1, col1 = path[i]
        row2, col2 = path[i + 1]
        x1 = col1 * CELL_SIZE + CELL_SIZE // 2
        y1 = row1 * CELL_SIZE + CELL_SIZE // 2
        x2 = col2 * CELL_SIZE + CELL_SIZE // 2
        y2 = row2 * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 5)
        pygame.display.update()
        time.sleep(0.1)


# Visualize multiple paths (step by step), if 2 agents have the same
# If two agents have the same destination cell on their path at a certain step, only the first agent's path is printed; the agents' paths are printed at the following steps.

CONFLICT_COLOR = (255, 0, 0)


def visualize_multi_path(screen, paths: Dict["Agent", List[Tuple[int, int]]]):
    max_steps = max(len(path) for path in paths.values())
    agent_colors = {
        agent: PATH_COLORS[i % len(PATH_COLORS)] for i, agent in enumerate(paths)
    }

    conflict_marker = {}  # Keeps track of conflicts for display

    for step in range(max_steps):
        current_positions = {}

        for agent, path in paths.items():
            if step < len(path):
                pos = path[step]
                if pos in current_positions:
                    # Conflict found, agent has to wait
                    conflict_marker[pos] = True
                else:
                    current_positions[pos] = agent
                    conflict_marker[pos] = False

        for pos, agent in current_positions.items():
            if conflict_marker[pos]:
                # Draw conflict marker
                row, col = pos
                x = col * CELL_SIZE + CELL_SIZE // 2
                y = row * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(screen, CONFLICT_COLOR, (x, y), CELL_SIZE // 4)
            else:
                # Draw agent path
                if step > 0:
                    prev_pos = paths[agent][step - 1]
                    pygame.draw.line(
                        screen,
                        agent_colors[agent],
                        (
                            prev_pos[1] * CELL_SIZE + CELL_SIZE // 2,
                            prev_pos[0] * CELL_SIZE + CELL_SIZE // 2,
                        ),
                        (
                            pos[1] * CELL_SIZE + CELL_SIZE // 2,
                            pos[0] * CELL_SIZE + CELL_SIZE // 2,
                        ),
                        5,
                    )

        pygame.display.update()
        time.sleep(1)

    # Finally, draw the full paths without conflicts
    for agent, path in paths.items():
        visualize_path(screen, path, agent_colors[agent])
