# File: ./src/main.py

# This file just show an example for running the Wumpus Game.

# main.py <-------------------------------------------
#     └─game.py
#           ├──agent.py
#           │      ├──knowledge_base.py
#           │      │      ├── utilities.py
#           │      │      ├── pysat.formula (external)
#           │      │      └── pysat.solvers (external)
#           │      └──inference_engine.py
#           │             ├── knowledge_base.py
#           │             └── utilities.py
#           ├──environment.py
#           │      └──utilities.py
#           ├──graphics_manager.py
#           │      ├──utilities.py
#           │      └──info_panel_graphics.py
#           │             └── pygame (external)
#           └── pygame (external)

from game import Game

if __name__ == "__main__":
    game = Game("../data/input/map7.txt")
    game.run()
