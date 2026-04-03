
from enum import Enum


class ChessPieceType(Enum):
    pawn   = 0
    knight = 1
    bishop = 2
    rook   = 3
    queen  = 4
    king   = 6


class ChessPieceColor(Enum):
    white = 0
    black = 1


class ChessPlayerColor(Enum):
    white = 0
    black = 1


class ChessPiece:
    """
    object that models a single chess-piece
    identified by a piece-type and color.
    """

    def __init__(self, type: ChessPieceType, color: ChessPieceColor) -> None:
        self.piece_type: ChessPieceType   = type
        self.piece_color: ChessPieceColor = color


    def to_fen(self) -> str:
        """
        converts a single piece to FEN-string notation.
        black pieces are lowercase-letters, white pieces uppercase letters.
        """
        res: str
        match (self.piece_type):
            case (ChessPieceType.pawn):
                res = "p"
            case (ChessPieceType.knight):
                res = "n"
            case (ChessPieceType.bishop):
                res = "b"
            case (ChessPieceType.rook):
                res = "r"
            case (ChessPieceType.queen):
                res = "q"
            case (ChessPieceType.king):
                res = "k"
        if (self.piece_color == ChessPieceColor.white):
            res = res.upper()
        return res