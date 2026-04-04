
# from app import App
# from graphics.scenes.chess_board import ChessBoardScene

# import pygame

# if __name__ == "__main__":
#     pygame.init()
#     app: App = App()
#     app.change_scene(ChessBoardScene)
#     app.exec()
#     pygame.quit()

import re

from gamelogic.pgn import PGNPatterns

test = """
[ iltam "sumra" ]
[ siltam "umra" ]

1. e4 2. e5
"""

blocks = re.search(PGNPatterns.pgn, test).groups()
)



