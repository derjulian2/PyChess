
from gamelogic.piece import ChessPieceColor, ChessPieceType, ChessPiece
from gamelogic.square import ChessSquare

from typing import Optional


class ChessBoard:
    """
    object that models the state of a regular chess-board.
    the default-value is a standard 8x8 chess-board with
    a starting-position setup.

    the board internally stores a ChessSquare object for every
    square on the board that may or may not hold a ChessPiece-instance,
    depending on wether a piece should stand on that square or not.
    """


    def __init__(self,
                 dimensions: tuple[int, int] = (8, 8)) -> None:
        self.pieces: dict[ChessSquare, ChessPiece] = dict()
        self.dimensions = dimensions
        self.__set_starting_position__()
    

    def __set_pawn_row__(self, color: ChessPieceColor, row: int) -> None:
        """
        sets a row to only pawns.

        :param color: the color of the pawns.
        :param row:   the rank to set.
        """
        for i in range(self.get_width()):
            self.pieces[ChessSquare(i, row)] = ChessPiece(ChessPieceType.pawn, color)


    def __set_back_row__(self, color: ChessPieceColor, row: int) -> None:
        """
        sets a row of 8-pieces to
        the standard-chess rook-to-rook back-rank layout.

        :param color: the color of the pieces.
        :param row:   the rank to set.
        """
        back_row = [
                ChessPiece(ChessPieceType.rook, color),
                ChessPiece(ChessPieceType.knight, color),
                ChessPiece(ChessPieceType.bishop, color),
                ChessPiece(ChessPieceType.queen, color),
                ChessPiece(ChessPieceType.king, color),
                ChessPiece(ChessPieceType.bishop, color),
                ChessPiece(ChessPieceType.knight, color),
                ChessPiece(ChessPieceType.rook, color)
        ]
        for i in range(len(back_row)):
            self.pieces[ChessSquare(i, row)] = back_row[i]


    def __set_starting_position__(self) -> None:
        """
        clears the board and sets a 
        standard chess starting-position.
        """
        self.clear()
        self.__set_pawn_row__(ChessPieceColor.white, 2)
        self.__set_pawn_row__(ChessPieceColor.black, 7)
        self.__set_back_row__(ChessPieceColor.white, 1)
        self.__set_back_row__(ChessPieceColor.black, 8)


    def __out_of_bounds__(self, sq: tuple[int, int]) -> bool:
        """
        performs a bounds-check on the passed square
        
        :param sq: the square to be checked.
        """
        if (sq[0] <= 0               or sq[1] <= 0 or
            sq[0] > self.get_width() or sq[1] > self.get_height()):
            return True
        return False
    

    def clear(self) -> None:
        """
        clears the entire board to just empty squares.
        """
        self.pieces.clear()


    def get_width(self) -> int:
        """
        :returns: the number of columns/files. default is 8.
        """
        return self.dimensions[0]
    

    def get_height(self) -> int:
        """
        :returns: the number of rows/ranks. default is 8.
        """
        return self.dimensions[1]


    def get_piece(self, sq: ChessSquare) -> Optional[ChessPiece]:
        """
        indexed and safe-guarded
        access to squares in column-row/file-rank format.
        
        making the parameter be of type ChessSquare allows
        ChessSquare.from_board('a1') to return the actual
        square corresponding to a1 here.
        
        :param sq: the square on the board to be queried.
        :returns:  the square on the board corresponding
                   to the passed square-instance.
        """
        if (self.__out_of_bounds__(sq)):
            raise ValueError("tried to get piece from out-of-bounds square")
        return self.pieces.get(sq)


    def square_has_piece(self, sq: ChessSquare) -> bool:
        return sq in self.pieces.keys()


    def get_pieces(self,
                   *,
                   color: Optional[ChessPieceColor] = None,
                   type: Optional[ChessPieceType]   = None) -> list[tuple[ChessSquare, ChessPiece]]:
        """
        access to all pieces on the board (optionially filtered).

        :param color: only include pieces of that color.
        :param type:  only include pieces of that type. 

        :returns: a list containing all squares with pieces that
                  are standing on the board (optionally satisfying color or type conditions).
        """
        res: list[tuple[ChessSquare, ChessPiece]] = [ (square, piece) for square, piece in self.pieces.values() ]
        if (color):
            res = filter(lambda elem: elem[1].get_color() == color, res)
        if (type):
            res = filter(lambda elem: elem[1].get_type() == type, res)
        return res
    
