
from dataclasses import dataclass
from enum import Enum, Flag
from typing import Self


class ChessColor(Enum):
    none  = 0
    white = 1
    black = 2


    def invert(self) -> Self:
        match (self):
            case (ChessColor.white):
                return ChessColor.black
            case (ChessColor.black):
                return ChessColor.white
        raise ValueError("cannot invert ChessColor.none")
    


class ChessGameState(Enum):
    in_progress = 0
    draw        = 1
    white_win   = 2
    black_win   = 3



class ChessPiece(Enum):
    none   = 0
    pawn   = 1
    knight = 2
    bishop = 3
    rook   = 4
    queen  = 5
    king   = 6



class ChessCastleSide(Flag):
    none      = 0
    kingside  = 0b1
    queenside = 0b10



@dataclass(frozen=True)
class ChessSquare:

    file: int
    rank: int


    @classmethod
    def from_str(cls, s: str) -> Self:
        if (len(s) != 2 or not (s[0].isalpha() and s[1].isdigit())):
            raise ValueError(f"cannot resolve square from {s}")
        if not (ord('a') <= ord(s[0]) <= ord('h')):
            raise ValueError(f"rank out-of-range: '{s}'")
        file = ord(s[0]) - (ord('a') - 1)
        rank = int(s[1])
        return cls(file, rank)
    

    def __post_init__(self) -> None:
        if not ((1 <= self.file <= 8) and (1 <= self.rank <= 8)):
           raise ValueError(f"square out-of-bounds: {self.file},{self.rank}")


    def __str__(self) -> str:
        return f"{chr(ord('a') + self.file - 1)}{self.rank}"