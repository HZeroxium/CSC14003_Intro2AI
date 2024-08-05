import pygame  # type: ignore
from agent import Agent
from environment import Environment
from graphics_manager import GraphicsManager
import time

class Game:
    def __init__(self, map_file):
        pygame.init()
        
        # Set up environment and agent
        self.env = Environment(map_file)
        self.agent = Agent(
            initial_position=self.env.get_agent_position(),
            grid_size=self.env.get_map_size()
        )
        
        # Set up graphics
        GraphicsManager.set_dimensions(self.env.get_map_size())
        self.screen = pygame.display.set_mode(
            (GraphicsManager.SCREEN_WIDTH, GraphicsManager.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Wumpus World")
        self.font = pygame.font.SysFont(None, GraphicsManager.FONT_SIZE)
        
        self.running = True
        self.next_step = False
        self.step = 0
        self.last_enter_press_time = 0
        self.current_delay = 0.5

    def run(self):
        self.display_initial_screen()
        
        while self.running and not (self.agent.is_game_over() or self.agent.is_game_won()):
            self.wait_for_next_step()
            if not self.running:
                break
            
            self.step += 1
            self.perform_step()
        
        self.display_final_screen()
        self.wait_for_exit()

    def display_initial_screen(self):
        """Display the initial screen with a 'Play' button."""
        self.screen.fill(GraphicsManager.BACKGROUND_COLOR)
        self.next_step_button = GraphicsManager.draw_centered_button(
            screen=self.screen,
            text="Play",
            size=(GraphicsManager.BUTTON_WIDTH, GraphicsManager.BUTTON_HEIGHT),
            color=GraphicsManager.GREEN,
        )
        pygame.display.update()
        

    def wait_for_next_step(self):
        """Wait for the user to click 'Play' or press Enter to proceed."""
        while not self.next_step:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()  # Ensure pygame shuts down properly
                    exit()  # Exit the program immediately
                if event.type == pygame.MOUSEBUTTONDOWN and self.next_step_button.collidepoint(event.pos):
                    self.next_step = True
                    self.current_delay = 0.5  # Reset delay for button click

            # Check if Enter key is pressed (held down)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                current_time = time.time()
                # Check if the specified delay time has passed since the last Enter key press
                if current_time - self.last_enter_press_time >= self.current_delay:
                    self.next_step = True
                    self.last_enter_press_time = current_time
                    # Decrease the delay by 10%, but not below 100ms
                    self.current_delay = max(self.current_delay * 0.9, 0.1)
            else:
                # Reset delay if Enter is not being pressed
                self.current_delay = 0.5

            pygame.display.update()

    def perform_step(self):
        """Perform the main game loop steps."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

        percepts = self.env.get_percept(self.agent.position)
        element = self.env.get_element(self.agent.position)
        actions = self.agent.choose_action(percepts, element)

        self.screen.fill(GraphicsManager.BACKGROUND_COLOR)
        GraphicsManager.draw_grid(self.env, self.agent, self.screen, self.font)
        GraphicsManager.draw_info_panel(self.agent, self.screen, self.font, self.env)

        # Draw 'Next Step' button
        next_step_button = GraphicsManager.draw_button(
            screen=self.screen,
            text="Next Step",
            size=(GraphicsManager.BUTTON_WIDTH, GraphicsManager.BUTTON_HEIGHT),
            pos=(
                GraphicsManager.SCREEN_WIDTH - GraphicsManager.BUTTON_WIDTH - 10,
                GraphicsManager.SCREEN_HEIGHT - GraphicsManager.BUTTON_HEIGHT - 10,
            ),
            color=GraphicsManager.YELLOW,
        )
        pygame.display.update()

        new_percept = self.env.update(self.agent, actions)
        self.agent.update_knowledge(new_percept)
        self.agent.log_actions()

        self.next_step = False

    def display_final_screen(self):
        """Display the final screen with the game result and an 'Exit' button."""
        final_message = "You won!" if self.agent.is_game_won() else "You lost!"
        self.screen.fill(GraphicsManager.BACKGROUND_COLOR)
        GraphicsManager.draw_text(
            self.screen,
            final_message,
            pygame.Rect(
                0,
                0,
                GraphicsManager.SCREEN_WIDTH,
                GraphicsManager.SCREEN_HEIGHT - 3 * GraphicsManager.BUTTON_HEIGHT,
            ),
            font=pygame.font.SysFont(None, 72),
        )

        exit_color = GraphicsManager.GREEN if self.agent.is_game_won() else GraphicsManager.RED
        exit_button = GraphicsManager.draw_centered_button(
            screen=self.screen,
            text="Exit",
            size=(GraphicsManager.BUTTON_WIDTH, GraphicsManager.BUTTON_HEIGHT),
            color=exit_color,
        )
        pygame.display.update()

        return exit_button
        
    def wait_for_exit(self):
        """Wait for the user to click 'Exit' to close the game."""
        exit_button = self.display_final_screen()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button.collidepoint(event.pos):
                        self.running = False  # Exit immediately when the "Exit" button is clicked
                        pygame.quit()  # Ensure pygame shuts down properly
                        exit()  # Exit the program immediately

            pygame.display.update()

if __name__ == "__main__":
    game = Game("../data/input/map5.txt")
    game.run()
