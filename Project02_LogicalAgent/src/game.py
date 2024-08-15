# File: ./src/game.py

# This file contains the main game loop for a "Wumpus World" game using Pygame.
# It handles initializing the game environment, agent, and graphics;
# running the game loop to process user inputs and agent actions;
# and displaying the initial, ongoing, and final game screens.
# Key functionalities include setting up the environment and agent, managing game steps and delays,
# processing user inputs, updating the game state, and rendering graphics and user interface elements.

# main.py
#     └─game.py <-------------------------------------------
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
#           │      └──info_panel_graphics.py
#           │             └── pygame (external)
#           └── pygame (external)

import pygame
from agent import Agent
from environment import Environment
from graphics_manager import GraphicsManager
import time


class Game:
    # Constants
    INITIAL_DELAY = 0.5  # Initial delay between steps in seconds
    MIN_DELAY = 0.05  # Minimum delay between steps in seconds
    DELAY_DECREASE_FACTOR = 0.9  # Factor by which the delay decreases (10%)
    FONT_SIZE = 72  # Font size for the final message
    TOP_LEFT_CORNER_X = 0
    TOP_LEFT_CORNER_Y = 0
    FINAL_SCREEN_MARGIN = 3
    FINAL_MESSAGE_FONT_SIZE = 72
    BUTTON_EXIT_WIN_COLOR = GraphicsManager.GREEN
    BUTTON_EXIT_LOSE_COLOR = GraphicsManager.RED

    def __init__(self, map_file):
        pygame.init()

        # Based on the input map file, create output file for actions
        # Example: input/map1.txt -> output/result1.txt
        self.output_file = map_file.replace("input", "output").replace("map", "result")
        # Set up environment and agent
        self.env = Environment(map_file)
        self.agent = Agent(
            initial_position=self.env.get_agent_position(),
            grid_size=self.env.get_map_size(),
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
        self.current_delay = Game.INITIAL_DELAY

        self.step_history = []  # List to track the last 20 steps

    def run(self):
        self.display_initial_screen()

        # Clear the output file
        open(self.output_file, "w").close()

        while self.running and not (
            self.agent.is_game_over() or self.agent.is_game_won()
        ):
            self.wait_for_next_step()
            if not self.running:
                break

            self.step += 1
            self.perform_step()

        # Write final score to the output file
        with open(self.output_file, "a") as file:
            file.write(f"Final Score: {self.agent.score}\n")

        self.display_final_screen()
        self.wait_for_exit()

    def display_initial_screen(self):
        """Display the initial screen with a 'Play' button."""
        self.screen.fill(GraphicsManager.BACKGROUND_COLOR)
        # Store the button as an instance variable for later access
        self.next_step_button = GraphicsManager.draw_centered_button(
            screen=self.screen,
            text="Play",
            size=(GraphicsManager.BUTTON_WIDTH, GraphicsManager.BUTTON_HEIGHT),
            color=GraphicsManager.GREEN,
        )
        pygame.display.update()

    def wait_for_next_step(self):
        """Wait for the user to click 'Next Step' or press Enter to proceed."""
        enter_key_pressed = False  # Flag to track if the Enter key was just pressed

        while not self.next_step:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()  # Ensure pygame shuts down properly
                    exit()  # Exit the program immediately

                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and self.next_step_button.collidepoint(event.pos)
                ):
                    self.next_step = True
                    self.current_delay = (
                        Game.INITIAL_DELAY
                    )  # Reset delay for button click

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    enter_key_pressed = True  # Enter key was just pressed

                if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                    self.current_delay = (
                        Game.INITIAL_DELAY
                    )  # Reset the delay when Enter is released

            # Check if Enter key is pressed (held down)
            keys = pygame.key.get_pressed()
            current_time = time.time()

            if enter_key_pressed or (
                keys[pygame.K_RETURN]
                and current_time - self.last_enter_press_time >= self.current_delay
            ):
                # Immediate step for key press or sufficient delay has passed for a hold
                self.next_step = True
                self.last_enter_press_time = current_time
                self.current_delay = max(
                    self.current_delay * Game.DELAY_DECREASE_FACTOR, Game.MIN_DELAY
                )

            pygame.display.update()

    def perform_step(self):
        """Perform the main game loop steps."""
        previous_position = self.agent.position  # Track the previous position

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

        percepts = self.env.get_percept(self.agent.position)
        element = self.env.get_element(self.agent.position)
        actions = self.agent.choose_action(percepts, element)

        # Update the step history with current step data
        self.step_history.append(f"#step[{self.step}] -> {self.agent.get_data()}")
        if len(self.step_history) > 20:  # Keep only the last 20 steps
            self.step_history.pop(0)

        self.screen.fill(GraphicsManager.BACKGROUND_COLOR)
        GraphicsManager.draw_grid(self.env, self.agent, self.screen, self.font)

        # Pass step history to the info panel
        GraphicsManager.draw_info_panel(
            self.agent,
            self.screen,
            self.font,
            self.env,
            self.agent.position,
            previous_position,
            self.step_history,
        )

        # Draw 'Next Step' button and store it as an instance variable
        self.next_step_button = GraphicsManager.draw_button(
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
        self.agent.log_actions(self.output_file)

        self.next_step = False

    def display_final_screen(self):
        """Display the final screen with the game result and an 'Exit' button."""
        final_message = (
            "You won!"
            if self.agent.is_game_won()
            else (
                "You fell into a pit!"
                if self.agent.fall_down
                else (
                    "You are eaten by the Wumpus!"
                    if self.agent.be_eaten
                    else "You lose!"
                )
            )
        )

        self.screen.fill(GraphicsManager.BACKGROUND_COLOR)
        GraphicsManager.draw_text(
            self.screen,
            final_message,
            pygame.Rect(
                Game.TOP_LEFT_CORNER_X,
                Game.TOP_LEFT_CORNER_Y,
                GraphicsManager.SCREEN_WIDTH,
                GraphicsManager.SCREEN_HEIGHT
                - Game.FINAL_SCREEN_MARGIN * GraphicsManager.BUTTON_HEIGHT,
            ),
            self.font,
            # self.font=pygame.font.SysFont(Game.FONT_SIZE, Game.FINAL_MESSAGE_FONT_SIZE),
        )

        """Display the final screen with the game result and an 'Exit' button."""
        if self.agent.is_game_won():
            final_image = pygame.image.load('../data/image/you_win.png')
        else:
            final_image = pygame.image.load('../data/image/game_over.png')

        final_image = pygame.transform.scale(
        final_image,
        (GraphicsManager.SCREEN_WIDTH // 4, GraphicsManager.SCREEN_HEIGHT // 4)
    )

        self.screen.fill(GraphicsManager.BACKGROUND_COLOR)
        self.screen.blit(final_image, (525, 100))

        exit_color = (
            Game.BUTTON_EXIT_WIN_COLOR
            if self.agent.is_game_won()
            else Game.BUTTON_EXIT_LOSE_COLOR
        )
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
                        self.running = (
                            False  # Exit immediately when the "Exit" button is clicked
                        )
                        pygame.quit()  # Ensure pygame shuts down properly
                        exit()  # Exit the program immediately

            pygame.display.update()
