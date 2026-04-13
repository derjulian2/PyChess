
from graphics.scenes.scene import Scene
from graphics.entities.board import ChessBoard

import chess.game as chess

from pygame_gui import UIManager
from asset_manager import AssetManager


class ChessBoardScene(Scene):
    """
    scene that draws the chess-board and
    the move-history UI to the player.
    """

    def __init__(self, 
                 ui_manager: UIManager, 
                 asset_manager: AssetManager) -> None:
        super().__init__(ui_manager, asset_manager)
        
        self.game: chess.ChessGame = chess.ChessGame()

        self.board = ChessBoard(self.game, (50, 50), 800)
