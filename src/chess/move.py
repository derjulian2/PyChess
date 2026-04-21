
from chess.common import ChessColor, ChessPiece, ChessSquare, ChessCastleSide

from dataclasses import dataclass
from typing import ClassVar, TypeAlias, Self


class InvalidMoveError(Exception):
    pass



@dataclass(frozen=True, )
class ChessMove:

    source: ChessSquare
    target: ChessSquare

    def __eq__(self, other: Self):
        """
        explicit definition because the other
        move-types inheriting from this still
        need to compare equal to another if
        the squares match.
        """
        return (self.source == other.source
                and self.target == other.target)
    

    def __str__(self):
        return f"{self.source}->{self.target}"



@dataclass(frozen=True)
class ChessMovePromotion(ChessMove):

    promotion: ChessPiece

    __valid_promotions__: ClassVar[list[ChessPiece]] = [
        ChessPiece.bishop, ChessPiece.knight, ChessPiece.rook, ChessPiece.queen
    ]

    def __post_init__(self) -> None:
        if not (self.promotion in ChessMovePromotion.__valid_promotions__):
            raise InvalidMoveError(f"cannot promote to '{self.promotion}'")


    def __str__(self):
        return f"{self.source}->{self.target}={self.promotion}"



@dataclass(frozen=True)
class ChessCastleSquares:
    king_source: ChessSquare
    king_target: ChessSquare
    rook_source: ChessSquare
    rook_target: ChessSquare



ChessCastleDescr: TypeAlias = tuple[ChessColor, ChessCastleSide]


class ChessMoveCastle(ChessMove):

    castle_to_squares: ClassVar[dict[ChessCastleDescr, ChessCastleSquares]] = {
        (ChessColor.white, ChessCastleSide.kingside)  
        : ChessCastleSquares(ChessSquare.from_str('e1'), ChessSquare.from_str('g1'),
                             ChessSquare.from_str('h1'), ChessSquare.from_str('f1')),
        
        (ChessColor.white, ChessCastleSide.queenside) 
        : ChessCastleSquares(ChessSquare.from_str('e1'), ChessSquare.from_str('c1'),
                             ChessSquare.from_str('a1'), ChessSquare.from_str('d1')),
        
        (ChessColor.black, ChessCastleSide.kingside)  
        : ChessCastleSquares(ChessSquare.from_str('e8'), ChessSquare.from_str('g8'),
                             ChessSquare.from_str('h8'), ChessSquare.from_str('f8')),
        
        (ChessColor.black, ChessCastleSide.queenside) 
        : ChessCastleSquares(ChessSquare.from_str('e8'), ChessSquare.from_str('c8'),
                             ChessSquare.from_str('a8'), ChessSquare.from_str('d8'))
    }

    squares_to_castle: ClassVar[dict[ChessMove, ChessCastleDescr]] = {
        ChessMove(sq.king_source, sq.king_target) : descr for descr, sq in castle_to_squares.items()
    }


    @classmethod
    def from_descr(cls, color: ChessColor, side: ChessCastleSide):
        sq = ChessMoveCastle.castle_to_squares.get((color, side))
        if (not sq):
            raise InvalidMoveError(f"invalid description for castling: '{color}, {side}'")
        return cls(sq.king_source, sq.king_target)
    

    def __post_init__(self) -> None:
        if not (self in ChessMoveCastle.castle_to_squares.values()):
            raise InvalidMoveError(f"invalid squares for castling: '{self.source}->{self.target}'")


    def descr(self) -> ChessCastleDescr:
        descr = ChessMoveCastle.squares_to_castle.get(ChessMove(self.source, self.target))
        if (not descr):
            raise ValueError(f"invalid ChessMoveCastle-instance: '{repr(self)}'")
        return descr


    def color(self) -> ChessColor:
        return self.descr()[0]


    def side(self) -> ChessCastleSide:
        return self.descr()[1]


    def __str__(self):
        if (self.side() == ChessCastleSide.kingside):
            return "O-O"
        elif (self.side() == ChessCastleSide.queenside):
            return "O-O-O"



@dataclass(frozen=True)
class ChessMoveEnPassant(ChessMove):

    en_passant: ChessSquare

    def __str__(self) -> str:
        return f"{self.source}->{self.target} e. p."