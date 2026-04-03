
from graphics.scenes.scene import Scene
from graphics.game_objects.board import ChessBoard
from graphics.game_objects.piece import ChessPiece

import gamelogic.piece as logic

from pygame_gui import UIManager
from asset_manager import AssetManager

class ChessBoardScene(Scene):
    """
    scene that draws the chess-board and
    the move-history UI to the player.
    """

    def __init__(self, ui_manager: UIManager, asset_manager: AssetManager) -> None:
        super().__init__(ui_manager, asset_manager)
        # self.board: ChessBoard
        # self.__setup_board__()

        self.test_piece = ChessPiece(asset_manager,
                                     logic.ChessPiece(logic.ChessPieceType.king, logic.ChessPieceColor.black),
                                     (100, 100), 100)
        self.attach_game_object(self.test_piece)


    def __setup_board__(self) -> None:
        self.board = ChessBoard()
        self.attach_game_object(self.board)


    def __setup_gui__(self) -> None:
        pass