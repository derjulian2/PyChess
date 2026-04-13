
from enum import Enum
from typing import Self
from dataclasses import dataclass, field


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



@dataclass
class ChessPiece:
    """
    object that models a single chess-piece
    identified by a piece-type and color.
    """

    type: ChessPieceType = field(default=ChessPieceType.pawn)
    color: ChessColor    = field(default=ChessColor.white)


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


    def __hash__(self) -> int:
        return hash((self.type, self.color))