
from chess.piece import ChessPiece, ChessPieceType, ChessColor
from chess.square import ChessSquare

from utility.vec import vec2

from typing import Callable, Optional, Iterable, Self
from enum import Flag


class InvalidMoveError(Exception):
    """
    exception-type that will be raised
    if a given move is not playable in
    a given position.
    """
    pass



class ChessMove(vec2[ChessSquare]):
    """
    an object representing a move on a chess-board
    defined by a starting-square and an end-square.
    """

    def __init__(self, *args) -> None:
        """
        inherits from utility.vec.vec2[ChessSquare], so any of the following
        construction-patterns is valid:
            ChessMove(ChessSquare('a1'), ChessSquare('b2'))   -> a1 to b2
            ChessMove((ChessSquare('a1'), ChessSquare('b2'))) -> a1 to b2
            ChessMove(ChessMove(...))                         -> a1 to b2

        additionally, from a string encoding a move in algebraic chess-notation:
            ChessMove('Qxe4') [NOT IMPLEMENTED YET]           -> Queen to e4
        """
        if (len(args) == 1 and isinstance(args[0], str)):
            super().__init__(None, None)
            self.from_algebraic(args[0])
        else:
            super().__init__(*args)


    def get_source_square(self) -> ChessSquare:
        """
        :returns: the square that contains the piece to be moved.
        """
        return self.x
    

    def get_target_square(self) -> ChessSquare:
        """
        :returns: the square to which the piece should be moved.
        """
        return self.y
    

    def from_algebraic(self, s: str) -> None:
        raise NotImplementedError()



class ChessCastleSide(Flag):
    """
    flag representing the side
    that a player castled on.
    """

    none      = 0
    kingside  = 0b01
    queenside = 0b10



class ChessMoveCastle(ChessMove):
    """
    specialization for representing
    a castling-move.
    """

    def __init__(self, side: ChessCastleSide) -> None:
        self.side: ChessCastleSide = side
        super.__init__(None)


    def get_side(self) -> ChessCastleSide:
        """
        :returns: the side that a player castles on.
        """
        return self.side



class ChessMovePromotion(ChessMove):
    """
    specialization for representing
    a promotion-move.
    """

    
    def __init__(self, squares: Iterable, piece: ChessPieceType) -> None:
        self.promotion: ChessPieceType = piece
        super().__init__(squares)


    def __validate_piece__(self) -> bool:
        """
        :returns: True if the piece promoted to is one of [ knight, bishop, rook, queen ].
        """
        

    def get_promotion(self) -> ChessPieceType:
        """
        :returns: the piece that the pawn was promoted to.
        """
        return self.promotion