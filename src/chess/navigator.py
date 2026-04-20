
from chess.common import ChessColor, ChessSquare, ChessCastleSide
from chess.bitboard import ChessBitBoard, ChessBitBoardPiece

from dataclasses import dataclass
from typing import Optional


@dataclass
class ChessBoardNavigator:
    """
    collection of utility-methods
    to generate piece-movement-patterns in ChessBoard.
    """

    board: ChessBitBoard
    sq: ChessSquare


    def __post_init__(self) -> None:
        self.__raise_if_no_piece__()


    def __raise_if_no_piece__(self) -> None:
        piece = self.board.get_square(self.sq)
        if (piece[1].is_none()):
            raise ValueError("cannot navigate from empty square")


    def __piece__(self) -> ChessBitBoardPiece:
        return self.board.get_square(self.sq)[1]


    def __is_initial_pawn_rank__(self) -> bool:
        piece = self.__piece__()
        return (piece.color == ChessColor.black and self.sq.rank == 7 or
                piece.color == ChessColor.white and self.sq.rank == 2)


    def __is_empty__(self, sq: ChessSquare) -> bool:
        return self.board.get_square(sq)[1].is_none()


    def __is_blocked_by_ally__(self, sq: ChessSquare) -> bool:
        piece       = self.__piece__()
        other_piece = self.board.get_square(sq)
        return piece.color == other_piece[1].color

    
    def __is_blocked_by_enemy__(self, sq: ChessSquare) -> bool:
        piece       = self.__piece__()
        other_piece = self.board.get_square(sq)
        return piece.color != other_piece[1].color and other_piece[1].color != ChessColor.none


    def __front__(self) -> int:
        if (self.__piece__().color == ChessColor.white):
            return 1
        else:
            return -1


    def castle(self, side: ChessCastleSide) -> list[ChessSquare]:
        res = list()
        if (side == ChessCastleSide.kingside):
            for i in range(3):
                res.append(ChessSquare(self.sq.file + i, self.sq.rank))
        elif (side == ChessCastleSide.queenside):
            for i in range(4):
                res.append(ChessSquare(self.sq.file - i, self.sq.rank))
        else:
            raise ValueError(f"invalid castling-side: '{side}'")
        return res
    

    def relative(self, 
                 dx: int = 0, 
                 dy: int = 0) -> Optional[ChessSquare]:
        try:    
            sq = ChessSquare(self.sq.file + dx, self.sq.rank + dy)
            if (self.__is_blocked_by_ally__(sq)): 
                return None
            elif (self.__is_blocked_by_enemy__(sq) 
                  or self.__is_empty__(sq)):
                return sq 
        except: 
            return None


    def advance(self, dy: int = 1) -> Optional[ChessSquare]:
        try:    
            sq = ChessSquare(self.sq.file, self.sq.rank + dy * self.__front__())
            if (self.__is_blocked_by_ally__(sq)
                or self.__is_blocked_by_enemy__(sq)):
                return None
            else:
                return sq 
        except: 
            return None


    def slide(self,
              dx: int = 0,
              dy: int = 0) -> list[ChessSquare]:
        res  = list()

        i    = 1
        iter = self.relative(i * dx, i * dy)
        while (iter):
            res.append(iter)
            i   += 1
            iter = self.relative(i * dx, i * dy)
        return res