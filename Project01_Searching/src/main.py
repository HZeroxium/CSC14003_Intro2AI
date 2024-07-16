import pygame  # type: ignore
from simulation.visualizer import run_level_screen, get_screen


if __name__ == "__main__":
    pygame.init()
    screen = get_screen()
    run_level_screen(screen)
