
from gamelogic.common import *
from gamelogic.square import ChessSquare
from enum import Enum

import re

"""
algebraic-chess-notation implemented with regular expressions.
maybe you can put this in a parser-generator and get something better from that?
doing this by hand is cumbersome, that's why regex.

[[:check_or_checkmate:]  := [#+]?
[[:kingside_castling:]]  := \A(0-0|O-O)[[:check_or_checkmate:]]$
[[:queenside_castling:]] := \A(0-0-0|O-O-O)[[:check_or_checkmate:]]$
[[:castling:]]           := [[:kingside_castling:]]|[[:queenside_castling]]

[[:takes:]] := [x]?
[[:piece:]] := [NBRQK]
[[:rank:]] := [a-h]
[[:file:]] := [1-8]
[[:target_square:]] := [:rank:][:file:]

[[:pawn_move:]] := \A[[:takes:]][[:target_square:]][[:check_or_checkmate:]]$
[[:piece_move:]] := \A[[:piece:]][[:takes:]][[:target_square:]][[:check_or_checkmate:]]$

[[:move:]] := [[:castling:]]|[[:pawn_move:]]|[[:piece_move:]]

the final move-regex will determine if a string encodes a valid chess-move. this
does not mean that this move is possible to perform on the current position, but only
that it is in legal algebraic chess notation.
"""

class ChessMoveType(Enum):
    regular          = 0
    capture          = 1
    kingside_castle  = (1 << 1)
    queenside_castle = (1 << 2)
    promotion        = (1 << 3)
    check            = (1 << 4)
    checkmate        = (1 << 5)
    
class ChessAlgebraicNotationPatterns:
    """
    for determining wether a string encodes
    a well-formed algebraic-chess-move we use regular-expressions.

    if this determines a string to be 'well-formed' that doesn't
    yet mean that the move is valid whatsoever. it just means, that
    it fits the language-pattern, nothing more yet.

    everything further will be decided on the board.
    """
    rank             = r"[1-8]"
    file             = r"[a-h]"
    square           = rf"{file}{rank}"
    
    check            = r"[#+]"
    takes            = r"[x]"
    piece            = r"[NBRQK]"
    promotion_pieces = r"[NBRQ]"

    castle           = rf"([O0]-[O0])|([O0]-[O0]-[O0])"
    regular_move     = (rf"(?P<piece>{piece})?"
                        + rf"(?P<source>{file}|{rank}|{square})?"
                        + rf"(?P<takes>{takes})?"
                        + rf"(?P<target>{square})")
    
    promotion        = rf"(?P<promotion>(={promotion_pieces})|(\({promotion_pieces}\))|({promotion_pieces}))"

    algebraic_move   = rf"^(?P<move>({regular_move}{promotion}?)|({castle}))(?P<check>{check})?$"


class ChessMove:


    def __init__(self) -> None:
        self.target_square: ChessSquare
        self.piece: ChessPieceType
        self.type: ChessMoveType


    @classmethod
    def from_algebraic(cls, move: str):
        """
        constructs a move from algebraic chess-notation.
        """
        pass