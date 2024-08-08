import pygame

# COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)



# X,Y position
HEALTHBAR_X_Index = 800
HEALTHBAR_Y_Index = 35

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

    def get_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def get_health(self, amount):
        if self.target_health < self.maximum_health:
            self.target_health += amount
        if self.target_health > self.maximum_health:
            self.target_health = self.maximum_health

    def update_health_bar(self, screen, agent_health):
        self.target_health = agent_health  # Ensure target_health is updated with the agent's health

        transition_width = 0
        transition_color = RED

        if self.current_health < self.target_health:
            self.current_health = min(self.current_health + self.health_change_speed, self.target_health)
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = GREEN
        elif self.current_health > self.target_health:
            self.current_health = max(self.current_health - self.health_change_speed, self.target_health)
            transition_width = int((self.current_health - self.target_health) / self.health_ratio)
            transition_color = YELLOW

        health_bar_rect = pygame.Rect(HEALTHBAR_X_Index, HEALTHBAR_Y_Index, self.current_health / self.health_ratio, 25)
        transition_bar_rect = pygame.Rect(health_bar_rect.right, HEALTHBAR_Y_Index, transition_width, 25)

        pygame.draw.rect(screen, RED, health_bar_rect)
        pygame.draw.rect(screen, transition_color, transition_bar_rect)
        pygame.draw.rect(screen, BLACK, (HEALTHBAR_X_Index, HEALTHBAR_Y_Index, self.health_bar_length, 25), 4)

