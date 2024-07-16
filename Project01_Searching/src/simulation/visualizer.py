import pygame  # type: ignore
import time
from citymap import CityMap, CellType
from typing import List, Tuple, Dict
from simulation.multiple_agents import Agent
import numpy as np  # type: ignore
from collections import deque

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
    (201, 30, 14),
    (15, 212, 205),
    (212, 133, 15),
    (107, 212, 15),
    (15, 212, 107),
    (212, 15, 186),
    (15, 71, 212),
    (133, 15, 212),
    (212, 15, 113),
]

TRANSPARENCY = 100


CONFLICT_SYMBOL = "X"


def draw_grid(screen, city_map: CityMap, font):
    i = 0
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

    # Draw start and goal cells of each agent with different colors

    n = len(city_map.start_points)
    for i in range(n):
        start = city_map.start_points[i]
        goal = city_map.goal_points[i]
        pygame.draw.rect(
            screen,
            PATH_COLORS[i % len(PATH_COLORS)],
            (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )
        pygame.draw.rect(
            screen,
            PATH_COLORS[i % len(PATH_COLORS)],
            (goal[1] * CELL_SIZE, goal[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )
        text_surface = font.render(str(i), True, TEXT_COLOR)
        text_rect = text_surface.get_rect(
            center=(
                start[1] * CELL_SIZE + CELL_SIZE // 2,
                start[0] * CELL_SIZE + CELL_SIZE // 2,
            )
        )
        screen.blit(text_surface, text_rect)
        text_surface = font.render(str(i), True, TEXT_COLOR)
        text_rect = text_surface.get_rect(
            center=(
                goal[1] * CELL_SIZE + CELL_SIZE // 2,
                goal[0] * CELL_SIZE + CELL_SIZE // 2,
            )
        )
        screen.blit(text_surface, text_rect)


def visualize_path(screen, city_map: CityMap, path, color=PATH_COLOR):
    if not path:
        return

    for i in range(len(path) - 1):
        row1, col1 = path[i]
        row2, col2 = path[i + 1]
        x1 = col1 * CELL_SIZE + CELL_SIZE // 2
        y1 = row1 * CELL_SIZE + CELL_SIZE // 2
        x2 = col2 * CELL_SIZE + CELL_SIZE // 2
        y2 = row2 * CELL_SIZE + CELL_SIZE // 2

        cell1 = city_map.get_cell((row1, col1))
        cell2 = city_map.get_cell((row2, col2))

        if cell1.type == CellType.EMPTY and cell2.type == CellType.EMPTY:
            pygame.draw.line(screen, color, (x1, y1), (x2, y2), 5)
        else:
            # Draw half lines
            if cell1.type == CellType.EMPTY:
                mid_x = (x1 + x2) // 2
                mid_y = (y1 + y2) // 2
                pygame.draw.line(screen, color, (x1, y1), (mid_x, mid_y), 5)
            if cell2.type == CellType.EMPTY:
                mid_x = (x1 + x2) // 2
                mid_y = (y1 + y2) // 2
                pygame.draw.line(screen, color, (mid_x, mid_y), (x2, y2), 5)

        pygame.display.update()
        time.sleep(0.1)


def average_color(colors: List[Tuple[int, int, int]]) -> Tuple[int, int, int]:
    """
    Calculate the average color from a list of RGB color tuples.
    """
    if not colors:
        return (0, 0, 0)
    r = int(np.mean([color[0] for color in colors]))
    g = int(np.mean([color[1] for color in colors]))
    b = int(np.mean([color[2] for color in colors]))
    return (r, g, b)


def visualize_multi_path(screen, city_map, paths: Dict["Agent", List[Tuple[int, int]]]):
    max_steps = max(len(path) for path in paths.values())
    agent_colors = {
        agent: PATH_COLORS[i % len(PATH_COLORS)] for i, agent in enumerate(paths)
    }

    # Initialize the matrix to keep track of cell colors
    cell_colors = {}

    for step in range(max_steps):
        current_positions = {}
        waiting_agents = []

        for agent, path in paths.items():
            if step < len(path):
                pos = path[step]
                if pos in current_positions:
                    # Conflict found, agent has to wait
                    waiting_agents.append(agent)
                else:
                    current_positions[pos] = agent

        for agent in waiting_agents:
            if step > 0:
                # Add the current position again to simulate waiting
                paths[agent].insert(step, paths[agent][step - 1])

        # Check for direction conflicts and update paths accordingly
        for agent, path in paths.items():
            if step < len(path) - 1:
                current_pos = path[step]
                next_pos = path[step + 1]

                for other_agent, other_path in paths.items():
                    if other_agent != agent and step < len(other_path) - 1:
                        other_current_pos = other_path[step]
                        other_next_pos = other_path[step + 1]

                        if (
                            current_pos == other_next_pos
                            and next_pos == other_current_pos
                        ):
                            # Conflict found, agent has to wait
                            paths[other_agent].insert(step + 1, other_current_pos)
                            other_path.insert(step + 1, other_current_pos)

        for pos, agent in current_positions.items():
            row, col = pos
            if pos in cell_colors:
                cell_colors[pos].append(agent_colors[agent])
            else:
                cell_colors[pos] = [agent_colors[agent]]

            avg_color = average_color(cell_colors[pos])

            # Draw the path with the average color
            if step > 0:
                prev_pos = paths[agent][step - 1]
                prev_row, prev_col = prev_pos

                cell1 = city_map.get_cell((prev_row, prev_col))
                cell2 = city_map.get_cell((row, col))

                if cell1.type == CellType.EMPTY and cell2.type == CellType.EMPTY:
                    pygame.draw.line(
                        screen,
                        avg_color,
                        (
                            prev_col * CELL_SIZE + CELL_SIZE // 2,
                            prev_row * CELL_SIZE + CELL_SIZE // 2,
                        ),
                        (
                            col * CELL_SIZE + CELL_SIZE // 2,
                            row * CELL_SIZE + CELL_SIZE // 2,
                        ),
                        5,
                    )
                else:
                    # Draw half lines
                    if cell1.type == CellType.EMPTY:
                        mid_x = (
                            prev_col * CELL_SIZE + col * CELL_SIZE + CELL_SIZE
                        ) // 2
                        mid_y = (
                            prev_row * CELL_SIZE + row * CELL_SIZE + CELL_SIZE
                        ) // 2
                        pygame.draw.line(
                            screen,
                            avg_color,
                            (
                                prev_col * CELL_SIZE + CELL_SIZE // 2,
                                prev_row * CELL_SIZE + CELL_SIZE // 2,
                            ),
                            (mid_x, mid_y),
                            5,
                        )
                    if cell2.type == CellType.EMPTY:
                        mid_x = (
                            prev_col * CELL_SIZE + col * CELL_SIZE + CELL_SIZE
                        ) // 2
                        mid_y = (
                            prev_row * CELL_SIZE + row * CELL_SIZE + CELL_SIZE
                        ) // 2
                        pygame.draw.line(
                            screen,
                            avg_color,
                            (mid_x, mid_y),
                            (
                                col * CELL_SIZE + CELL_SIZE // 2,
                                row * CELL_SIZE + CELL_SIZE // 2,
                            ),
                            5,
                        )

        pygame.display.update()
        time.sleep(0.5)


def visualize_multi_path_optimized(screen, paths: Dict["Agent", List[Tuple[int, int]]]):
    max_steps = max(len(path) for path in paths.values())
    agent_colors = {
        agent: PATH_COLORS[i % len(PATH_COLORS)] for i, agent in enumerate(paths)
    }

    # Initialize the matrix to keep track of cell colors and waiting agents
    cell_colors = {}
    waiting_counts = {}

    for step in range(max_steps):
        current_positions = {}
        waiting_agents = []

        for agent, path in paths.items():
            if step < len(path):
                pos = path[step]
                if pos in current_positions:
                    # Conflict found, agent has to wait
                    waiting_agents.append(agent)
                    waiting_counts[pos] = waiting_counts.get(pos, 0) + 1
                else:
                    current_positions[pos] = agent

        for agent in waiting_agents:
            if step > 0:
                # Add the current position again to simulate waiting
                paths[agent].insert(step, paths[agent][step - 1])

        # Check for direction conflicts and update paths accordingly
        for agent, path in paths.items():
            if step < len(path) - 1:
                current_pos = path[step]
                next_pos = path[step + 1]

                for other_agent, other_path in paths.items():
                    if other_agent != agent and step < len(other_path) - 1:
                        other_current_pos = other_path[step]
                        other_next_pos = other_path[step + 1]

                        if (
                            current_pos == other_next_pos
                            and next_pos == other_current_pos
                        ):
                            # Conflict found, agent has to wait
                            paths[other_agent].insert(step + 1, other_current_pos)
                            other_path.insert(step + 1, other_current_pos)

        for pos, agent in current_positions.items():
            row, col = pos
            if pos in cell_colors:
                cell_colors[pos].append(agent_colors[agent])
            else:
                cell_colors[pos] = [agent_colors[agent]]

            avg_color = average_color(cell_colors[pos])

            # Draw the path with the average color
            if step > 0:
                prev_pos = paths[agent][step - 1]
                prev_row, prev_col = prev_pos

                if row == prev_row or col == prev_col:  # Horizontal or vertical line
                    pygame.draw.line(
                        screen,
                        avg_color,
                        (
                            prev_col * CELL_SIZE + CELL_SIZE // 2,
                            prev_row * CELL_SIZE + CELL_SIZE // 2,
                        ),
                        (
                            col * CELL_SIZE + CELL_SIZE // 2,
                            row * CELL_SIZE + CELL_SIZE // 2,
                        ),
                        5,
                    )
                else:  # Intersection point
                    pygame.draw.circle(
                        screen,
                        avg_color,
                        (
                            col * CELL_SIZE + CELL_SIZE // 2,
                            row * CELL_SIZE + CELL_SIZE // 2,
                        ),
                        CELL_SIZE // 4,
                    )

            # Draw the current location of the agent
            pygame.draw.circle(
                screen,
                agent_colors[agent],
                (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                CELL_SIZE // 4,
            )

        # Display waiting information
        for pos, count in waiting_counts.items():
            if count > 0:
                font = pygame.font.SysFont(None, 24)
                text = font.render(f"Wait: {count}", True, (0, 0, 0))
                screen.blit(text, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE))
            else:
                waiting_counts.pop(pos, None)

        pygame.display.update()
        time.sleep(2)
