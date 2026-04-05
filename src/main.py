
from app import App
from graphics.scenes.board import ChessBoardScene

import pygame

if __name__ == "__main__":
    pygame.init()
    app: App = App()
    app.change_scene(ChessBoardScene)
    app.exec()
    pygame.quit()


