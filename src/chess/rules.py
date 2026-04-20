
from chess.common import ChessCastleSide, ChessColor, ChessPiece, ChessSquare
from chess.move import ChessMove, ChessMoveCastle, ChessMoveEnPassant, InvalidMoveError
from chess.board import ChessBoard
from chess.navigator import ChessBoardNavigator

from abc import ABC
from typing import ClassVar
from copy import deepcopy

from dataclasses import dataclass, field
from random import randint


class ChessRule(ABC):

    def validate(self, mv: ChessMove, board: ChessBoard) -> None:
        pass

    def update(self, mv: ChessMove, board: ChessBoard) -> None:
        pass



class PieceRule(ChessRule):

    def validate(self, mv: ChessMove, board: ChessBoard) -> None:
        src = board.get_square(mv.source)
        tgt = board.get_square(mv.target)
        
        if (src[1].is_none()):
            raise InvalidMoveError("no piece standing on source-square")

        if not (tgt[1].is_none()):
            if (src[1].color == tgt[1].color):
                raise InvalidMoveError("target is blocked by allied piece")
            if (tgt[1].piece == ChessPiece.king):
                raise InvalidMoveError("king is standing on target")
            


class MoveRule(ChessRule):
    """
    exceptions to this rule: castling and en-passant
    """

    def validate(self, mv: ChessMove, board: ChessBoard) -> None:
        if not (isinstance(mv, ChessMoveCastle) or isinstance(mv, ChessMoveEnPassant)):
            if not (mv in board.gen_moves(mv.source)):
                raise InvalidMoveError("cannot move piece to unreachable square")



class PlayerToMoveRule(ChessRule):

    color: ChessColor = ChessColor.white


    def validate(self, mv: ChessMove, board: ChessBoard) -> None:
        piece = board.get_square(mv.source)
        if (piece[1].color != self.color):
            raise InvalidMoveError("moved piece doesn't match player-to-move")
        

    def update(self, mv: ChessMove, board: ChessBoard) -> None:
        self.color = self.color.invert()



@dataclass
class EnPassantRule(ChessRule):

    moves: list[ChessMoveEnPassant] = field(default_factory=list)

    @staticmethod
    def is_double_pawn_move(mv: ChessMove, board: ChessBoard) -> bool:
        piece = board.get_square(mv.source)[1]
        if (piece.piece == ChessPiece.pawn):
            return abs(mv.source.rank - mv.target.rank) == 2
        return False


    def is_possible(self) -> bool:
        return len(self.moves) != 0


    def validate(self, mv: ChessMove, board: ChessBoard) -> None:
        if (isinstance(mv, ChessMoveEnPassant)):
            if not (self.is_possible()):
                raise InvalidMoveError(f"invalid en-passant: '{mv}'")
            elif (self.is_possible() and mv not in self.moves):
                raise InvalidMoveError(f"invald en-passant: '{mv}', possible: '{",".join(self.moves)}'")


    def update(self, mv: ChessMove, board: ChessBoard) -> None:
        if (EnPassantRule.is_double_pawn_move(mv, board)):
            nav = ChessBoardNavigator(board, mv.source)
            en_passant_target  = nav.advance()
            en_passant_sources = board.__gen_en_passant_squares_pawn__(nav)
            en_passant_taken   = mv.target
            for en_passant_source in en_passant_sources:
                self.moves.append(ChessMoveEnPassant(en_passant_source, en_passant_target, en_passant_taken))
        elif (self.is_possible()):
            self.moves.clear()
            




@dataclass
class CastleRule(ChessRule):

    default_rights: ClassVar[dict[ChessColor, ChessCastleSide]] = {
        ChessColor.white : ChessCastleSide.kingside | ChessCastleSide.queenside,
        ChessColor.black : ChessCastleSide.kingside | ChessCastleSide.queenside
    }

    rights: dict[ChessColor, ChessCastleSide] = field(default_factory=lambda: CastleRule.default_rights)


    def validate(self, mv: ChessMove, board: ChessBoard) -> None:
        if (isinstance(mv, ChessMoveCastle)):
            if (not self.rights[mv.color()] & mv.side()):
                if (randint(1, 5) == 1):
                    raise InvalidMoveError("you don't have the right O you don't have the right," \
                                           "therefore you don't have the right, O you don't have the right")
                else:
                    raise InvalidMoveError("no right to castle")
            if (not board.can_castle((mv.color(), mv.side()))):
                raise InvalidMoveError("cannot castle in the current position")


    def update(self, mv: ChessMove, board: ChessBoard) -> None:
        piece = board.get_square(mv.source)[1]
        if (piece.is_none()):
            return
        
        if (self.rights[piece.color] != ChessCastleSide.none):
            if (isinstance(mv, ChessMoveCastle)):
                self.rights[piece.color] = ChessCastleSide.none
            
            if (piece.piece == ChessPiece.rook):
                if (mv.source.file == 8):
                    self.rights[piece.color] &= ~ChessCastleSide.kingside
                elif (mv.source.file == 1):
                    self.rights[piece.color] &= ~ChessCastleSide.queenside
            elif (piece.piece == ChessPiece.king):
                self.rights[piece.color] = ChessCastleSide.none



class CheckRule(ChessRule):

    def validate(self, mv: ChessMove, board: ChessBoard) -> None:
        piece = board.get_square(mv.source)[1]
        tmp = deepcopy(board)
        tmp.make_move(mv)
        if (board.in_check(piece.color)):
            if (tmp.in_check(piece.color)):
                raise InvalidMoveError("move does not resolve check")
        else:
            if (tmp.in_check(piece.color)):
                raise InvalidMoveError("move would put the king in check")
        