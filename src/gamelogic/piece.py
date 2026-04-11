
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
                 type: ChessPieceType, 
                 color: ChessColor) -> None:
        self.type: ChessPieceType   = type
        self.color: ChessColor      = color


    def __str__(self) -> str:
        """
        conversion to string.
        :returns: a single character denoting the type
                  and color of the piece. 
                  lowercase for black, uppercase for white.
        """
        match (self.get_type()):
            case (ChessPieceType.pawn):
                res = "P"
            case (ChessPieceType.knight):
                res = "N"
            case (ChessPieceType.bishop):
                res = "B"
            case (ChessPieceType.rook):
                res = "R"
            case (ChessPieceType.queen):
                res = "Q"
            case (ChessPieceType.king):
                res = "K"
        if (self.get_color() == ChessColor.black):
            res = res.lower()
        return res


    def get_type(self) -> ChessPieceType:
        """
        getter for the type of piece.
        """
        return self.type


    def get_color(self) -> ChessColor:
        """
        getter for piece-color.
        """
        return self.color


