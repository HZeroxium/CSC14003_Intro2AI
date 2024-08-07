import pygame

class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((240, 240, 240))
        self.rect = self.image.get_rect(center=(400, 400))
        self.current_health = 200
        self.target_health = 200
        self.maximum_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health_change_speed = 5

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

    def update_health_bar(self, screen):
        transition_width = 0
        transition_color = (255, 0, 0)
        isGetHealth = False

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (0, 255, 0)
            isGetHealth = True
        elif self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.current_health - self.target_health) / self.health_ratio)
            transition_color = (255, 255, 0)

        health_bar_rect = pygame.Rect(10, 45, (self.current_health if isGetHealth else self.target_health) / self.health_ratio, 25)
        transition_bar_rect = pygame.Rect(health_bar_rect.right, 45, transition_width, 25)

        pygame.draw.rect(screen, (255, 0, 0), health_bar_rect)
        pygame.draw.rect(screen, transition_color, transition_bar_rect)
        pygame.draw.rect(screen, (255, 255, 255), (10, 45, self.health_bar_length, 25), 4)
