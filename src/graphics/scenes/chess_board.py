
from graphics.scenes.scene import Scene
from graphics.game_objects.board import ChessBoard

import gamelogic.game as logic

from pygame_gui import UIManager
from asset_manager import AssetManager

class ChessBoardScene(Scene):
    """
    scene that draws the chess-board and
    the move-history UI to the player.
    """

    def __init__(self, ui_manager: UIManager, asset_manager: AssetManager) -> None:
        super().__init__(ui_manager, asset_manager)
        
        self.game: logic.ChessGame = logic.ChessGame()

        self.board = ChessBoard(asset_manager, self.game.board, (100, 100), 800)
        self.attach_game_object(self.board)


    def __setup_board__(self) -> None:
        self.board = ChessBoard()
        self.attach_game_object(self.board)


    def __setup_gui__(self) -> None:
        pass