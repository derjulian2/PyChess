
from chess.common import ChessColor, ChessPiece, ChessSquare

from dataclasses import dataclass
from typing import Self, TypeAlias, Optional


@dataclass(frozen=True)
class ChessBitBoardPiece:

    color: ChessColor
    piece: ChessPiece
    
    @classmethod
    def none(cls) -> Self:
        return cls(ChessColor.none, ChessPiece.none)
    

    def __post_init__(self) -> None:
        if (self.color != ChessColor.none and self.piece == ChessPiece.none or
            self.color == ChessColor.none and self.piece != ChessPiece.none):    
            raise ValueError(f"invalid piece-description: '{self.color, self.piece}'")


    def is_none(self) -> bool:
        return self.color == ChessColor.none and self.piece == ChessPiece.none



ChessBitBoardSquare: TypeAlias = tuple[ChessSquare, ChessBitBoardPiece]
ChessBitBoardRank: TypeAlias   = list[ChessBitBoardSquare]
ChessBitBoardFile: TypeAlias   = list[ChessBitBoardSquare]


class ChessBitBoard:
    """
    the state of the board is stored as 64 instances
    of (ChessColor, ChessPiece)-tuples which all
    represent a single square on the board.
    """

    def __init__(self) -> None:
        self.data: list[ChessBitBoardPiece]                      = list()
        self.pieces: dict[ChessColor, list[ChessBitBoardSquare]] = dict()
        self.__reset__()


    def __reset__(self) -> None:
        self.data = [ ChessBitBoardPiece(ChessColor.none, ChessPiece.none) for _ in range(64) ]
        self.pieces = {
            ChessColor.white : list(),
            ChessColor.black : list()
        }
        

    @staticmethod
    def __to_index__(sq: ChessSquare) -> int:
        """
        ranks/files start at 1 and end at 8.
        named adjustment for indexed-access.
        """
        return 8 * (sq.rank - 1) + (sq.file - 1)
    

    def get_square(self, sq: ChessSquare) -> ChessBitBoardSquare:
        return (sq, self.data[ChessBitBoard.__to_index__(sq)])


    def set_square(self, sq: ChessSquare, pc: ChessBitBoardPiece) -> None:
        old = self.get_square(sq)
        if not (old[1].is_none()):
            self.pieces[old[1].color].remove(old)
        if not (pc.is_none()):
            self.pieces[pc.color].append((sq, pc))
        self.data[ChessBitBoard.__to_index__(sq)] = pc
        

    def get_file(self, file: int) -> ChessBitBoardFile:
        return [ self.get_square(ChessSquare(file, i)) for i in range(1, 9) ]
    

    def get_rank(self, rank: int) -> ChessBitBoardRank:
        return [ self.get_square(ChessSquare(i, rank)) for i in range(1, 9) ]
    

    def get_pieces(self, 
                   color: Optional[ChessColor] = None, 
                   piece: Optional[ChessPiece] = None) -> list[ChessBitBoardSquare]:
        res: list[ChessBitBoardSquare] = self.pieces[ChessColor.black] + self.pieces[ChessColor.white]
        if (color and color != ChessColor.none):
            res = self.pieces[color]
        if (piece and piece != ChessPiece.none):
            res = set(filter(lambda sq: sq[1].piece == piece, res))
        return res