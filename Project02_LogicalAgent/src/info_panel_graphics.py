# File: ./src/info_panel_graphics.py

# This file defines the `HealthBar` class, which manages the graphical representation of the agent's health bar 
# in the "Wumpus World" game using Pygame. It includes functionality to initialize the health bar, update it based on 
# the agent's current health, and visually transition the health bar when health changes occur. 
# The health bar is displayed on the screen and visually updates to reflect the agent's health status.

# main.py
#     └─game.py 
#           ├──agent.py 
#           │      └──inference_engine.py
#           │             ├── knowledge_base.py
#           │             │       ├── utilities.py
#           │             │       ├── pysat.formula (external)
#           │             │       └── pysat.solvers (external)
#           │             └── utilities.py
#           ├──environment.py
#           │      └──utilities.py
#           ├──graphics_manager.py
#           │      ├──utilities.py
#           │      └──info_panel_graphics.py <-------------------------------------------
#           │             └── pygame (external)
#           └── pygame (external)

import pygame

# COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# X,Y position
HEALTH_BAR_X_INDEX = 750
HEALTH_BAR_Y_INDEX = 35
HEART_ICON_X_INDEX = 710
HEART_ICON_Y_INDEX = 35

class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((240, 240, 240))
        self.rect = self.image.get_rect(center=(400, 400))
        self.current_health = 100
        self.target_health = 100
        self.maximum_health = 100
        self.health_bar_length = 400
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health_change_speed = 10


    def update_health_bar(self, screen, agent_health):
        self.target_health = agent_health  # Ensure target_health is updated with the agent's health

        transition_width = 0
        transition_color = RED
        isGetHealth = False

        if self.current_health < self.target_health:
            self.current_health = min(self.current_health + self.health_change_speed, self.target_health)
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = GREEN
            isGetHealth = True
        elif self.current_health > self.target_health:
            self.current_health = max(self.current_health - self.health_change_speed, self.target_health)
            transition_width = int((self.current_health - self.target_health) / self.health_ratio)
            transition_color = YELLOW

        health_bar_rect = pygame.Rect(HEALTH_BAR_X_INDEX, HEALTH_BAR_Y_INDEX, (self.current_health if isGetHealth else self.target_health) / self.health_ratio, 25)
        transition_bar_rect = pygame.Rect(health_bar_rect.right, HEALTH_BAR_Y_INDEX, transition_width, 25)

        pygame.draw.rect(screen, RED, health_bar_rect)
        pygame.draw.rect(screen, transition_color, transition_bar_rect)
        pygame.draw.rect(screen, BLACK, (HEALTH_BAR_X_INDEX, HEALTH_BAR_Y_INDEX, self.health_bar_length, 25), 4)

        # Draw health as heart icons
        heart_icon = pygame.image.load(f"../data/image/heart_{self.target_health}.png")
        screen.blit(heart_icon, (HEART_ICON_X_INDEX, HEART_ICON_Y_INDEX))
