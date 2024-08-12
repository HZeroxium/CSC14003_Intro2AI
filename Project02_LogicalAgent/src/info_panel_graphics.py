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
GOLD = (218, 109, 0)

# X,Y position
HEALTH_BAR_X_INDEX = 750
HEALTH_BAR_Y_INDEX = 5
HEART_ICON_X_INDEX = 710
HEART_ICON_Y_INDEX = 5
GOLD_ICON_X_INDEX  = 710
GOLD_ICON_Y_INDEX  = 35
SCORE_ICON_X_INDEX = 698
SCORE_ICON_Y_INDEX = 65
COMPASS_ICON_X_INDEX = 715
COMPASS_ICON_Y_INDEX = 95
MOVEMENT_ICON_X_INDEX = 770
MOVEMENT_ICON_Y_INDEX = 107


class Info_Panel():
    def __init__(self):
        self.health_bar = HealthBar()
        self.gold = Gold()
        self.score = Score()
        self.movements = Movements()
    
    def update_info_panel(self, screen, agent):
        self.health_bar.update_health_bar(screen, agent.health)
        self.gold.update_gold(screen, agent)
        self.score.update_score(screen)
        self.movements.update_movements(screen, agent)


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

class Gold():
    def __init__(self) -> None:
        pass

    def update_gold(self, screen, agent):
        gold_icon = pygame.image.load(f"../data/image/gold.png")
        screen.blit(gold_icon, (GOLD_ICON_X_INDEX, GOLD_ICON_Y_INDEX))

        if agent._is_gold(agent.position):
            monospace_font = pygame.font.SysFont("Courier New", 14)
            surface = monospace_font.render('+5000', True, GOLD)
            
            screen.blit(surface, (GOLD_ICON_X_INDEX + (60 if len(agent.grabbed_gold) == 0 else
                                                       80 if len(agent.grabbed_gold) * 5000 <= 5000 
                                                       else 100),
                                  GOLD_ICON_Y_INDEX + 5))
            

class Score():
    def __init__(self) -> None:
        pass

    @staticmethod
    def update_score(screen):
        score_icon = pygame.image.load(f"../data/image/score.png")
        screen.blit(score_icon, (SCORE_ICON_X_INDEX, SCORE_ICON_Y_INDEX))


class Movements():
    def __init__(self) -> None:
        self.direction = ['NORTH', 'EAST', 'SOUTH', 'WEST']
        self.current_direction = 0
        pass

    def update_movements(self, screen, agent):
        actions = agent.get_action_string().split(', ')

        forward_direction = {
            'FORWARD_NORTH': 'UP',
            'FORWARD_EAST': 'RIGHT',
            'FORWARD_SOUTH': 'DOWN',
            'FORWARD_WEST': 'LEFT'
        }

        for i, a in enumerate(actions):
            if a == 'FORWARD':
                action_icon = pygame.image.load(f"../data/image/{forward_direction[a + "_" + self.direction[self.current_direction] ]}.png")
                screen.blit(action_icon, (30 * i + MOVEMENT_ICON_X_INDEX, MOVEMENT_ICON_Y_INDEX))
            elif a == 'TURN_LEFT':
                self.current_direction = (self.current_direction + 4 - 1) % 4
                rotate_icon = pygame.image.load(f'../data/image/{a}.png')
                screen.blit(rotate_icon, (30 * i + MOVEMENT_ICON_X_INDEX, MOVEMENT_ICON_Y_INDEX))
            elif a == 'TURN_RIGHT':
                self.current_direction = (self.current_direction + 4 + 1) % 4
                rotate_icon = pygame.image.load(f'../data/image/{a}.png')
                screen.blit(rotate_icon, (30 * i + MOVEMENT_ICON_X_INDEX, MOVEMENT_ICON_Y_INDEX))
            else:
                grab_icon = pygame.image.load(f'../data/image/{a}.png')
                screen.blit(grab_icon, (30 * i + MOVEMENT_ICON_X_INDEX, MOVEMENT_ICON_Y_INDEX))

        compass_icon = pygame.image.load(f"../data/image/compass.png")
        screen.blit(compass_icon, (COMPASS_ICON_X_INDEX, COMPASS_ICON_Y_INDEX))