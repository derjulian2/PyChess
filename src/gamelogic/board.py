
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
        self.pieces: list[ChessPiece] = list()
        self.__set_starting_position__()
    

    def __clear_board__(self) -> None:
        """
        clears the entire board to just empty squares.
        """
        self.pieces.clear()
        

    def __set_starting_position__(self) -> None:
        """
        clears the board and sets a standard chess starting-position.
        """
        # helper-functions to generate by color
        def get_pawn_row(color: ChessPieceColor, row: int) -> list[ChessPiece]:
            return [ ChessPiece(ChessPieceType.pawn, color, ChessSquare(i + 1, row)) for i in range(self.board_columns) ]

        def get_back_row(color: ChessPieceColor, row: int) -> list[ChessPiece]:
            return [
                ChessPiece(ChessPieceType.rook, color, ChessSquare(1, row)),
                ChessPiece(ChessPieceType.knight, color, ChessSquare(2, row)),
                ChessPiece(ChessPieceType.bishop, color, ChessSquare(3, row)),
                ChessPiece(ChessPieceType.queen, color, ChessSquare(4, row)),
                ChessPiece(ChessPieceType.king, color, ChessSquare(5, row)),
                ChessPiece(ChessPieceType.bishop, color, ChessSquare(6, row)),
                ChessPiece(ChessPieceType.knight, color, ChessSquare(7, row)),
                ChessPiece(ChessPieceType.rook, color, ChessSquare(8, row))
            ]
        
        self.__clear_board__()
        self.pieces += get_pawn_row(ChessPieceColor.white, 2)
        self.pieces += get_pawn_row(ChessPieceColor.black, 7)
        self.pieces += get_back_row(ChessPieceColor.white, 1)
        self.pieces += get_back_row(ChessPieceColor.black, 8)


    def to_fen(self) -> str:
        """
        returns the board's state in FEN-string notation.
        """
        res: str = str()
        empty_squares: int = 0
        
        # # small helper-function
        # def flush_empty_squares_if() -> None:
        #     nonlocal res, empty_squares
        #     if (empty_squares != 0):
        #         res += str(empty_squares)
        #         empty_squares = 0

        # for row in self.rows:
        #     for square in row:
        #         if square is None:
        #             empty_squares += 1
        #         else:
        #             flush_empty_squares_if()
        #             res += square.to_fen()
        #     flush_empty_squares_if()
        #     if (row is not self.rows[-1]):
        #         res += "/"
        return res

    """
    information-queries.
    """

    def get_pieces(self) -> list[ChessPiece]:
        """
        returns a list containing all pieces that
        are left on the board.
        """
        return self.pieces