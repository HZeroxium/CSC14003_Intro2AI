import sys
import time
import pygame
import threading
from utils import format_path
from multiagent.cbs import cbs
from typing import List, Tuple, Dict
from citymap import CityMap, CellType
from simulation.multiple_agents import Agent
from simulation.multiple_agents import get_agents
from search_algorithms import bfs, dfs, ucs, gbfs, a_star

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
    (200, 72, 72),  # Bright Red
    (3, 219, 252),  # Bright Green
    (72, 72, 200),  # Bright Blue
    (200, 200, 72),  # Yellow
    (200, 72, 200),  # Magenta
    (72, 200, 200),  # Cyan
    (128, 72, 128),  # Purple
    (200, 165, 72),  # Orange
    (72, 128, 128),  # Teal
]

# Constants for the screens
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
MARGIN = 20

# Constants for the simulation
INFO_BOX_WIDTH = 300
INFO_BOX_HEIGHT = SCREEN_HEIGHT

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (220,20,60)
GREEN = (0, 255, 0)
BLUE = (0, 128, 255)

# Global variable to control the timer and path-counter
timer_running = False

# Global variable to control the step of visualization
pause = True
show_all = False
exit = False


# Function to get the screen
def get_screen():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Search Algorithm Visualization")
    return screen


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


# Function to visualize the path of a single agent
def single_agent(screen, city_map: CityMap, output: str, level: int = 1):
    global pause, show_all, exit

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

    # Add buttons
    next_button = draw_button(
        screen,
        "Next",
        (SCREEN_WIDTH - 150, 300),
        (BUTTON_WIDTH, BUTTON_HEIGHT),
    )
    all_button = draw_button(
        screen,
        "All",
        (SCREEN_WIDTH - 150, 380),
        (BUTTON_WIDTH, BUTTON_HEIGHT),
    )
    exit_button = draw_button(
        screen,
        "Exit",
        (SCREEN_WIDTH - 150, 460),
        (BUTTON_WIDTH, BUTTON_HEIGHT),
        RED
    )
    pygame.display.update()

    i = 0
    paths = {}
    start = city_map.start
    goal = city_map.goal
    for name, algorithm in algorithms[level].items():
        if level == 1:
            path = algorithm(city_map, start, goal)
        elif level <= 3:
            path = algorithm(city_map, start, goal, level)

        visualize_path(screen, next_button, all_button, exit_button, city_map, path, PATH_COLORS[i])
        pygame.display.update()

        if exit == True:
            break

        pygame.time.wait(1000)
        i += 1
        paths[name] = path

    show_all = False
    exit = False
    # Update the next button to show "Done"
    done_button = draw_button(
        screen,
        "Done",
        (SCREEN_WIDTH - 150, 300),
        (BUTTON_WIDTH, BUTTON_HEIGHT),
        GREEN,
    )
    pygame.display.update()

    with open(output, "w") as f:
        for name, path in paths.items():
            f.write(f"{name}: {format_path(path)}\n")
            f.write("Path length: {}\n".format(len(path) - 1))


def strip_agent_names(solution):
    stripped_solution = {}
    for key, value in solution.items():
        # Strip the agent name part from the key
        new_key = key.split(": ")[1] if ": " in key else key
        stripped_solution[new_key] = value
    return stripped_solution


def convert_solution_to_dict(agents: List[Agent], solution):
    agent_path_dict = {}
    agent_names = [f"agent{index}" for index, _ in enumerate(agents)]

    for agent_name, agent in zip(agent_names, agents):
        # Create a string that matches the format used as keys in the solution
        agent_description = f"{agent_name}: ({agent.start[0]}, {agent.start[1]}) -> ({agent.goal[0]}, {agent.goal[1]}):"

        # Extract the path string from the solution using the formatted description
        path_str = ""
        for key in solution:
            if key.startswith(agent_name):
                path_str = solution[key]
                break

        # Debug prints
        print(f"Agent Description: {agent_description}")
        print(f"Path String: {path_str}")

        # If a path is found, parse it into a list of tuples
        if path_str:
            path_list = parse_path_from_description(path_str)
            agent_path_dict[agent] = path_list
        else:
            agent_path_dict[agent] = []  # If no path, return an empty list

    return agent_path_dict


def parse_path_from_description(path_str):
    # Extract the path part from the string
    path_part = path_str.split(": ")[1].split("\n")[0]
    # Convert the path string into a list of tuples
    path_tuples = [
        tuple(map(int, point.strip("()").split(", ")))
        for point in path_part.split(" -> ")
    ]
    return path_tuples


def parse_path(path_str):
    # Converts path string "x, y -> x, y -> ..." into list of tuples [(x, y), (x, y), ...]
    return [
        tuple(map(int, coord.split(", "))) for coord in path_str.strip().split(" -> ")
    ]


# Function to format the path into a dictionary
def format_path(path):
    return " -> ".join(f"({x}, {y})" for x, y in path)


# Function to visualize the paths of multiple agents
def multiple_agent(screen, city_map: CityMap, output: str, filepath: str):
    agents = get_agents(city_map)
    raw_solution = cbs(filepath, output)  # Get raw solution from CBS

    print("Raw Solution from CBS:")
    print(raw_solution)
    print("---------------------------------------------------------------")
    # Convert the raw solution into the required dictionary format
    paths = convert_solution_to_dict(agents, raw_solution)

    print("Formatted Paths for Each Agent:")
    for agent, path in paths.items():
        print(f"Agent {agent.id} Path:")
        for step, pos in enumerate(path):
            print(f"  Step {step}: Position {pos}")
    print("---------------------------------------------------------------")

    # Visualize and handle the paths as required
    visualize_multi_path(screen, city_map, paths)


# Main function to run the level screen
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


# Main function to run the input file screen
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


# Main function to run the simulation screen
def run_simulation_screen(screen, level=None, input_file=None):
    global timer_running

    if level and input_file:
        filepath = f"../data/input/{input_file}"
        city_map = CityMap.from_file(filepath)

        screen_width = city_map.cols * CELL_SIZE + INFO_BOX_WIDTH
        screen_height = max(city_map.rows * CELL_SIZE, SCREEN_HEIGHT)
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Search Algorithm Visualization")

        font = pygame.font.SysFont(None, 24)
        draw_grid(screen, city_map, font)
        draw_info_box(screen, city_map.cols * CELL_SIZE)
        pygame.display.update()

        output = f"../data/output/output{input_file.split('_')[0][-1]}_level{level}.txt"

        start_time = time.time()
        timer_running = True
        timer_thread = threading.Thread(target=timer_function, args=(screen, city_map.cols, start_time))
        timer_thread.start()

        if int(level) >= 1 and int(level) <= 3:
            single_agent(screen, city_map, output, int(level))
        else:
            multiple_agent(screen, city_map, output, filepath)

        timer_running = False
        timer_thread.join()

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

# Helper function to update the real-time timer on the screen
def timer_function(screen, city_map_cols, start_time):
    global timer_running
    font = pygame.font.SysFont(None, 36)
    
    while timer_running:
        elapsed_time = time.time() - start_time
        timer_text_surface = font.render('{:.3f} s'.format(elapsed_time), True, BLACK)
        timer_text_rect = timer_text_surface.get_rect(topleft=(city_map_cols * CELL_SIZE + 130, 150))
        
        # Clear the previous timer text
        pygame.draw.rect(screen, WHITE, timer_text_rect)
        screen.blit(timer_text_surface, timer_text_rect)
        
        pygame.display.update()
        time.sleep(0.1)  # Update every 0.1 second


# Helper function to draw the information box
def draw_info_box(screen, width):
    # Draw the background for the info box
    info_box_rect = pygame.Rect(width, 0, INFO_BOX_WIDTH, INFO_BOX_HEIGHT)
    pygame.draw.rect(screen, BACKGROUND_COLOR, info_box_rect)  # Set background to white

    # Display information in the info box
    font = pygame.font.SysFont(None, 36)

    timer_text_surface = font.render('Time : ', True, BLACK)
    timer_text_rect = timer_text_surface.get_rect(topleft=(width + 50, 150))
    screen.blit(timer_text_surface, timer_text_rect)


# Helper function to draw the grid on the screen
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
                if celltype == CellType.FUEL_STATION:
                    str_value = "F" + str_value
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
        text_surface = font.render("S" + str(i), True, TEXT_COLOR)
        text_rect = text_surface.get_rect(
            center=(
                start[1] * CELL_SIZE + CELL_SIZE // 2,
                start[0] * CELL_SIZE + CELL_SIZE // 2,
            )
        )
        screen.blit(text_surface, text_rect)
        text_surface = font.render("G" + str(i), True, TEXT_COLOR)
        text_rect = text_surface.get_rect(
            center=(
                goal[1] * CELL_SIZE + CELL_SIZE // 2,
                goal[0] * CELL_SIZE + CELL_SIZE // 2,
            )
        )
        screen.blit(text_surface, text_rect)


# Helper function to visualize a single agent path on the screen
def visualize_path(screen, next_button, all_button, exit_button, city_map: CityMap, path, color=PATH_COLOR):
    if not path:
        return

    global pause, show_all, exit  
    
    for i in range(len(path) - 1):
        pause = True

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

        while pause and not show_all:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if next_button.collidepoint(event.pos):
                        pause = False
                    elif all_button.collidepoint(event.pos):
                        show_all = True
                    elif exit_button.collidepoint(event.pos):
                        exit = True
                        return

        time.sleep(0.1)

# Helper functions for visualizing multiple agents, calculate average color for overlapping paths
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
    screen, city_map: CityMap, paths: Dict[Agent, List[Tuple[int, int]]]
):
    global pause, show_all, exit    

    max_steps = max(len(path) for path in paths.values())
    agent_colors = {
        agent: PATH_COLORS[i % len(PATH_COLORS)] for i, agent in enumerate(paths)
    }

    # Add buttons
    next_button = draw_button(
        screen,
        "Next",
        (SCREEN_WIDTH - 150, 300),
        (BUTTON_WIDTH, BUTTON_HEIGHT),
    )
    all_button = draw_button(
        screen,
        "All",
        (SCREEN_WIDTH - 150, 380),
        (BUTTON_WIDTH, BUTTON_HEIGHT),
    )
    exit_button = draw_button(
        screen,
        "Exit",
        (SCREEN_WIDTH - 150, 460),
        (BUTTON_WIDTH, BUTTON_HEIGHT),
        RED
    )
    pygame.display.update()

    step = 0
    pause = True
    show_all = False
    exit = False
    # Initialize the matrix to keep track of cell colors
    cell_colors = {}
    for step in range(max_steps):
        while pause and not show_all:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if next_button.collidepoint(event.pos):
                        pause = False
                    elif all_button.collidepoint(event.pos):
                        show_all = True
                    elif exit_button.collidepoint(event.pos):
                        exit = True
                        return
        for agent, path in paths.items():
            if step < len(path):
                pos = path[step]
                row, col = pos
                # agent_color = agent_colors[agent]

                # if pos in cell_colors:
                #     cell_colors[pos].append(agent_color)
                # else:
                #     cell_colors[pos] = [agent_color]

                avg_color = PATH_COLORS[agent.id % len(PATH_COLORS)]

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
        pause = True

        if step == max_steps - 1:
            show_all = True
            # Update the next button to show "Done"
            done_button = draw_button(
                screen,
                "Done",
                (SCREEN_WIDTH - 150, 300),
                (BUTTON_WIDTH, BUTTON_HEIGHT),
                GREEN,
            )
            pygame.display.update()
