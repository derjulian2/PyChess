
from graphics.game_objects.piece import *

class ChessBoard(GameObject):
    """
    game-object that represents
    a chess-board with all it's pieces.
    """

    def __init__(self) -> None:
        self.pieces: list[ChessPiece] = list()

    