import pygame  # type: ignore
from agent import Agent
from environment import Environment
from graphics_manager import GraphicsManager

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
                    break
                if (
                    (event.type == pygame.MOUSEBUTTONDOWN and self.next_step_button.collidepoint(event.pos))
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN)
                ):
                    self.next_step = True

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
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN and exit_button.collidepoint(event.pos):
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    running = False

        pygame.display.update()

if __name__ == "__main__":
    game = Game("../data/input/map5.txt")
    game.run()
