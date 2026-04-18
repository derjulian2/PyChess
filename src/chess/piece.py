
from enum import Enum
from typing import Self


class ChessPieceType(Enum):
    """
    enum encoding the types
    of chess-pieces.
    """

    pawn   = 0
    knight = 1
    bishop = 2
    rook   = 3
    queen  = 4
    king   = 6



class ChessColor(Enum):
    """
    enum encoding the
    color of chess-pieces.
    """

    white = 0
    black = 1

    def invert(self) -> Self:
        return ChessColor(not self.value)



class ChessPiece:
    """
    object that models a single chess-piece
    identified by a piece-type and color.
    """

    def __init__(self, 
                 piece_type: ChessPieceType,
                 piece_color: ChessColor) -> None:
        self.type: ChessPieceType  = piece_type
        self.color: ChessColor     = piece_color


    def get_type(self) -> ChessPieceType:
        """
        :returns: an enum encoding what kind of piece this object is.
        """
        return self.type


    def get_color(self) -> ChessColor:
        """
        :returns: the color of the player that this piece belongs to.
        """
        return self.color


    def __hash__(self) -> int:
        """
        hash-overload for dictionary-compatibility.
        """
        return hash((self.get_type(), self.get_color()))