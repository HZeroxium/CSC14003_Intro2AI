import pygame  # type: ignore
import time
from citymap import CityMap, CellType
from typing import List, Tuple, Dict
from simulation.multiple_agents import Agent
import sys
import time
from search_algorithms import bfs, dfs, ucs, gbfs, a_star
from utils import format_path
from simulation.multiple_agents import (
    get_agents,
    simple_a_star_multi_agent,
    complex_a_star_multi_agent,
)

from simulation.test import cbs_multiple_agent

# Constants
CELL_SIZE = 60
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
    (200, 72, 72),       # Bright Red
    (72, 200, 72),       # Bright Green
    (72, 72, 200),       # Bright Blue
    (200, 200, 72),     # Yellow
    (200, 72, 200),     # Magenta
    (72, 200, 200),     # Cyan
    (128, 72, 128),     # Purple
    (200, 165, 72),     # Orange
    (72, 128, 128),     # Teal
]

# Constants for the screens
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 240
BUTTON_HEIGHT = 60
MARGIN = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 128, 255)


def get_screen():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Search Algorithm Visualization")
    return screen


def draw_button(screen, text, pos, size, color=GRAY):
    font = pygame.font.SysFont(None, 36)
    rect = pygame.Rect(pos, size)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    return rect


def single_agent(screen, city_map: CityMap, output: str, level: int = 1):
    algorithms = {
        1: {
            "BFS": bfs.bfs,
            "DFS": dfs.dfs,
            "UCS": ucs.ucs,
            "GBFS": gbfs.gbfs,
            "AStar": a_star.a_star,
        },
        2: {
            "AStar": a_star.a_star,
        },
        3: {
            "AStar": a_star.a_star,
        },
    }

    i = 0
    paths = {}
    start = city_map.start
    goal = city_map.goal
    for name, algorithm in algorithms[level].items():
        if level == 1:
            path = algorithm(city_map, start, goal)
        elif level <= 3:
            path = algorithm(city_map, start, goal, level)
        visualize_path(screen, city_map, path, PATH_COLORS[i])
        pygame.display.update()
        pygame.time.wait(1000)
        i += 1
        paths[name] = path

    with open(output, "w") as f:
        for name, path in paths.items():
            f.write(f"{name}: {format_path(path)}\n")
            f.write("Path length: {}\n".format(len(path) - 1))

    run_simulation_screen(screen)


def multiple_agent(screen, city_map: CityMap, output: str):
    agents = get_agents(city_map)
    # paths = a_star_multi_agent(city_map, agents)

    algorithms = {
        "Simple A*": simple_a_star_multi_agent,
        "Complex A*": complex_a_star_multi_agent,
        "CBS": cbs_multiple_agent,
    }
    algorithm = algorithms["CBS"]
    paths = algorithm(city_map, agents)
    visualize_multi_path(screen, city_map, paths)

    with open(output, "w") as f:
        for agent, path in paths.items():
            f.write(f"{agent}: {format_path(path)}\n")
            f.write("Path length: {}\n".format(len(path)))

    run_simulation_screen(screen)


def run_level_screen(screen):
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 48)
    text_surface = font.render("Select Level", True, BLACK)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(text_surface, text_rect)

    levels = ["Level 1", "Level 2", "Level 3", "Level 4"]
    buttons = []
    for i, level in enumerate(levels):
        button_rect = draw_button(
            screen,
            level,
            (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 150 + i * (BUTTON_HEIGHT + MARGIN)),
            (BUTTON_WIDTH, BUTTON_HEIGHT),
        )
        buttons.append((level, button_rect))

    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for level, rect in buttons:
                    if rect.collidepoint(event.pos):
                        run_input_file_screen(screen, level.split()[1])
                        return


def run_input_file_screen(screen, level):
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 48)
    text_surface = font.render(f"Select Input File for Level {level}", True, BLACK)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(text_surface, text_rect)

    input_files = [f"input{i}_level{level}.txt" for i in range(1, 6)]
    buttons = []
    for i, input_file in enumerate(input_files):
        button_rect = draw_button(
            screen,
            input_file,
            (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 100 + i * (BUTTON_HEIGHT + MARGIN)),
            (BUTTON_WIDTH, BUTTON_HEIGHT),
        )
        buttons.append((input_file, button_rect))

    back_button = draw_button(
        screen,
        "Back",
        (
            SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
            100 + len(input_files) * (BUTTON_HEIGHT + MARGIN),
        ),
        (BUTTON_WIDTH, BUTTON_HEIGHT),
        BLUE,
    )

    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for input_file, rect in buttons:
                    if rect.collidepoint(event.pos):
                        run_simulation_screen(screen, level, input_file)
                        return
                if back_button.collidepoint(event.pos):
                    run_level_screen(screen)
                    return


def run_simulation_screen(screen, level=None, input_file=None):
    if level and input_file:
        filepath = f"../data/input/{input_file}"
        city_map = CityMap.from_file(filepath)

        screen_width = city_map.cols * CELL_SIZE
        screen_height = city_map.rows * CELL_SIZE
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Search Algorithm Visualization")

        font = pygame.font.SysFont(None, 24)
        draw_grid(screen, city_map, font)
        pygame.display.update()

        output = f"../data/output/output{input_file.split('_')[0][-1]}_level{level}.txt"

        if int(level) >= 1 and int(level) <= 3:
            single_agent(screen, city_map, output, int(level))
        else:
            multiple_agent(screen, city_map, output)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # If the user presses the ESC key, back to input file screen
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run_level_screen(get_screen())
                return

    pygame.quit()
    sys.exit()


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
    r_sum = sum(color[0] for color in colors)
    r = int(r_sum / len(colors))
    g_sum = sum(color[1] for color in colors)
    g = int(g_sum / len(colors))
    b_sum = sum(color[2] for color in colors)
    b = int(b_sum / len(colors))
    return (r, g, b)


def visualize_multi_path(
    screen, city_map: CityMap, paths: Dict["Agent", List[Tuple[int, int]]]
):
    max_steps = max(len(path) for path in paths.values())
    agent_colors = {
        agent: PATH_COLORS[i % len(PATH_COLORS)] for i, agent in enumerate(paths)
    }

    # Initialize the matrix to keep track of cell colors
    cell_colors = {}

    for step in range(max_steps):
        for agent, path in paths.items():
            if step < len(path):
                pos = path[step]
                row, col = pos
                agent_color = agent_colors[agent]

                if pos in cell_colors:
                    cell_colors[pos].append(agent_color)
                else:
                    cell_colors[pos] = [agent_color]

                avg_color = average_color(cell_colors[pos])

                # Draw the path segment with the average color
                if step > 0:
                    prev_pos = path[step - 1]
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
                        # Draw half lines if one of the cells is not EMPTY
                        mid_x = (
                            prev_col * CELL_SIZE + col * CELL_SIZE + CELL_SIZE
                        ) // 2
                        mid_y = (
                            prev_row * CELL_SIZE + row * CELL_SIZE + CELL_SIZE
                        ) // 2

                        if cell1.type == CellType.EMPTY:
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
        pygame.time.wait(500)  # Adjust as needed for desired speed
