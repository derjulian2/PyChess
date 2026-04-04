
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


class ChessCharacterEncodings:

    piece_to_char: dict[tuple[ChessPieceColor, ChessPieceType], str] = {
        (ChessPieceColor.white, ChessPieceType.pawn)   : "P",
        (ChessPieceColor.white, ChessPieceType.knight) : "N",
        (ChessPieceColor.white, ChessPieceType.bishop) : "B",
        (ChessPieceColor.white, ChessPieceType.rook)   : "R",
        (ChessPieceColor.white, ChessPieceType.queen)  : "Q",
        (ChessPieceColor.white, ChessPieceType.king)   : "K",

        (ChessPieceColor.black, ChessPieceType.pawn)   : "p",
        (ChessPieceColor.black, ChessPieceType.knight) : "n",
        (ChessPieceColor.black, ChessPieceType.bishop) : "b",
        (ChessPieceColor.black, ChessPieceType.rook)   : "r",
        (ChessPieceColor.black, ChessPieceType.queen)  : "q",
        (ChessPieceColor.black, ChessPieceType.king)   : "k"
    }

    char_to_piece: dict[str, tuple[ChessPieceColor, ChessPieceType]] = {
        char : piece for piece, char in piece_to_char.items()
    }

