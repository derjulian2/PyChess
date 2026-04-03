
from enum import Enum

from gamelogic.piece import *


class ChessBoard:
    """
    object that models the state of a
    regular 8x8 chess-board.
    """
    
    board_rows    = 8
    board_columns = 8

    def __init__(self) -> None:
        self.rows: list[list[ChessPiece | None]] = list()
        self.__set_starting_position__()
    

    def __clear_board__(self) -> None:
        """
        clears the entire board to just empty squares.
        """
        self.rows.clear()
        for _ in range(ChessBoard.board_rows):
            row = [ None for __ in range(ChessBoard.board_columns) ]
            self.rows.append(row)


    def __set_starting_position__(self) -> None:
        """
        clears the board and sets a standard chess starting-position.
        """
        # helper-functions to generate by color
        def get_pawn_row(color: ChessPieceColor) -> list[ChessPiece]:
            return [ ChessPiece(ChessPieceType.pawn, color) for _ in range(self.board_columns) ]

        def get_back_row(color: ChessPieceColor) -> list[ChessPiece]:
            return [
                ChessPiece(ChessPieceType.rook, color),
                ChessPiece(ChessPieceType.knight, color),
                ChessPiece(ChessPieceType.bishop, color),
                ChessPiece(ChessPieceType.queen, color),
                ChessPiece(ChessPieceType.king, color),
                ChessPiece(ChessPieceType.bishop, color),
                ChessPiece(ChessPieceType.knight, color),
                ChessPiece(ChessPieceType.rook, color)
            ]
        
        self.__clear_board__()
        self.rows[-1] = get_back_row(ChessPieceColor.white)
        self.rows[-2] = get_pawn_row(ChessPieceColor.white)
        self.rows[0] = get_back_row(ChessPieceColor.black)
        self.rows[1] = get_pawn_row(ChessPieceColor.black)


    def to_fen(self) -> str:
        """
        returns the board's state in FEN-string notation.
        """
        res: str = str()
        empty_squares: int = 0
        
        # small helper-function
        def flush_empty_squares_if() -> None:
            nonlocal res, empty_squares
            if (empty_squares != 0):
                res += str(empty_squares)
                empty_squares = 0

        for row in self.rows:
            for square in row:
                if square is None:
                    empty_squares += 1
                else:
                    flush_empty_squares_if()
                    res += square.to_fen()
            flush_empty_squares_if()
            if (row is not self.rows[-1]):
                res += "/"
        return res
