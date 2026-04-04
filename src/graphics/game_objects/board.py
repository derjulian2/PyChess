
import gamelogic.board as logic

from graphics.game_objects.piece import *

class ChessBoard(GameObject):
    """
    game-object that represents
    a chess-board with all it's pieces.
    """
    
    def __init__(self,
                 asset_manager: AssetManager,
                 board: logic.ChessBoard,
                 pos: tuple[int, int],
                 size: float) -> None:
        super().__init__(self, asset_manager, Rect(pos, (size, size)))
        self.logical_board: logic.ChessBoard = board
        self.pieces: list[ChessPiece]        = list()

    
    def __

    