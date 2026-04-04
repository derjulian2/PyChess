
from gamelogic.common import *
from gamelogic.square import *
from gamelogic.move import *

class ChessPiece:
    """
    object that models a single chess-piece
    identified by a piece-type, color and square on the board.
    """

    def __init__(self, 
                 type: ChessPieceType, 
                 color: ChessPieceColor,
                 square: ChessSquare) -> None:
        self.type: ChessPieceType   = type
        self.color: ChessPieceColor = color
        self.square: ChessSquare    = square
        

    def to_fen(self) -> str:
        """
        converts a single piece to FEN-string notation.
        black pieces are lowercase-letters, white pieces uppercase letters.
        """
        res: str
        match (self.type):
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
        if (self.color == ChessPieceColor.white):
            res = res.upper()
        return res