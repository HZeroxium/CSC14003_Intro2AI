import sys
import pygame  # type: ignore
from citymap import CityMap
from simulation.visualizer import (
    draw_grid,
    visualize_path,
    CELL_SIZE,
    PATH_COLORS,
    visualize_multi_path,
)
from search_algorithms import bfs, dfs, ucs, gbfs, a_star
from utils import format_path
from simulation.multiple_agents import (
    get_agents,
    a_star_multi_agent,
)

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
        if level <= 3:
            path = algorithm(city_map, start, goal, level)
        visualize_path(screen, city_map, path, PATH_COLORS[i])
        pygame.display.update()
        pygame.time.wait(1000)
        i += 1
        paths[name] = path

    with open(output, "w") as f:
        for name, path in paths.items():
            f.write(f"{name}: {format_path(path)}\n")
            f.write("Path length: {}\n".format(len(path)))

    run_simulation_screen(screen)


def multiple_agent(screen, city_map: CityMap, output: str):
    agents = get_agents(city_map)
    paths = a_star_multi_agent(city_map, agents)
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


if __name__ == "__main__":
    pygame.init()
    screen = get_screen()
    run_level_screen(screen)
