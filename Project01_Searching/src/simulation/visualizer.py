import pygame
import time
from citymap import CityMap, CellType

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


def visualize_path(screen, path, font):
    for i in range(len(path) - 1):
        row1, col1 = path[i]
        row2, col2 = path[i + 1]
        x1 = col1 * CELL_SIZE + CELL_SIZE // 2
        y1 = row1 * CELL_SIZE + CELL_SIZE // 2
        x2 = col2 * CELL_SIZE + CELL_SIZE // 2
        y2 = row2 * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.line(screen, PATH_COLOR, (x1, y1), (x2, y2), 5)
        pygame.display.update()
        time.sleep(0.1)
