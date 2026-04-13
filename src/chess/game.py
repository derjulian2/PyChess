
from chess.piece  import ChessColor, ChessColor, ChessPieceType
from chess.square import ChessSquare
from chess.board  import ChessBoard
from chess.move   import ChessMove, InvalidMoveError, ChessMoveCastle, ChessMovePromotion

from typing import Optional, Self
from copy import copy
from dataclasses import dataclass, field


@dataclass
class ChessRule:
    """
    object that models a rule
    that has to be obeyed when
    making a move.

    rules can be dependent on each other
    (for example a move is OK if it the piece that was
     moved is now on a reachable square OR if a special move
     (like en-passant or a initial double-pawn-push) was played).

    this behaviour is reflected in a
    rule-tree that is constructed in ChessGame.
    """

    board: ChessBoard
    rule_exceptions: list[Self] = field(default_factory=list)


    def violated_by(self, mv: ChessMove) -> bool:
        """
        :returns: True if any of the subrules was violated.
        """
        return True in [ rule.violated_by(mv) for rule in self.rule_exceptions ]


    def react(self, mv: ChessMove) -> None:
        for rule in self.rule_exceptions:
            rule.react(mv)


class BoundsRule(ChessRule):
    """
    a move cannot start or end
    out-of-bounds.
    """

    def violated_by(self, mv: ChessMove) -> bool:
        return (self.board.is_out_of_bounds(mv.get_source_square()) or
                self.board.is_out_of_bounds(mv.get_target_square()))
    


class PieceRule(ChessRule):
    """
    a move cannot start from an
    empty square.
    """

    def violated_by(self, mv: ChessMove) -> bool:
        return not self.board.has_piece(mv.get_source_square())
    


class AlliedPieceRule(ChessRule):
    """
    a move cannot take an allied piece.
    """

    def violated_by(self, mv: ChessMove) -> bool:
        if (self.board.has_piece(mv.get_target_square())):
            src_piece = self.board.get_piece(mv.get_source_square())
            tgt_piece = self.board.get_piece(mv.get_target_square())
            return src_piece.get_color() == tgt_piece.get_color()
        


class KingRule(ChessRule):
    """
    a move cannot take a king-piece.
    """

    def violated_by(self, mv: ChessMove) -> bool:
        if (self.board.has_piece(mv.get_target_square())):
            src_piece = self.board.get_piece(mv.get_source_square())
            tgt_piece = self.board.get_piece(mv.get_target_square())
            return tgt_piece.get_type() == ChessPieceType.king
        


class InCheckRule(ChessRule):
    """
    the king cannot move
    to a square that would result in
    him being takeable in the next move.
    """

    def violated_by(self, mv: ChessMove) -> bool:
        src_piece = self.board.get_piece(mv.get_source_square())
        if (src_piece.get_type() == ChessPieceType.king):
            return self.board.is_attacked(src_piece.get_color(), mv.get_target_square())
        


class ResolveCheckRule(ChessRule):
    """
    a move is invalid if the king is currently 
    in check, but the played move
    does not resolve that check.
    """

    def violated_by(self, mv: ChessMove) -> bool:
        src_piece = self.board.get_piece(mv.get_source_square())
        if (self.board.is_in_check(src_piece.get_color())):
            cpy = copy(self.board)
            cpy.apply_move(mv)
            return cpy.is_in_check(src_piece.get_color())
        return False



class ReachableRule(ChessRule):

    
    def violated_by(self, mv: ChessMove) -> bool:
        # exceptions for StartingPawnRule and CheckRule or sth
        return mv.get_target_square() not in self.board.find_takeable(mv.get_source_square())



class CastlingRule(ChessRule):

    def __init__(self, board):
        super().__init__(board)
        self.rights = 0


class StartingPawnRule(ChessRule):

    def violated_by(self, mv: ChessMove) -> bool:
        piece = self.board.get_piece(mv.get_source_square())
        if (piece.get_type() == ChessPieceType.pawn):
            delta = abs(mv.get_source_square() - mv.get_target_square())
            if (delta == (2, 0)):
                return mv.get_source_square().get_rank() == self.board.get_initial_pawn_rank(piece.get_color())
        return False


class PromotionRule(ChessRule):

    def violated_by(self, mv: ChessMovePromotion) -> bool:
        if not (isinstance(mv, ChessMovePromotion)):
            return False
        
        promotion_options = [ ChessPieceType.knight, ChessPieceType.bishop, ChessPieceType.rook, ChessPieceType.queen]
        if (mv.promotion not in promotion_options):
            return True
        
        piece = self.board.get_piece(mv.get_source_square())
        if (piece.get_type() != ChessPieceType.pawn):
            return True
        
        if (piece.get_color() == ChessColor.white):
            last_rank = self.board.get_rank_count()
            second_last_rank = last_rank - 1
        else:
            last_rank = 1
            second_last_rank = last_rank + 1

        if (mv.get_source_square().get_rank() != second_last_rank):
            return True
        if (mv.get_target_square().get_rank() != last_rank):
            return True
        return False
        

class EnPassantRule(ChessRule):

    def __init__(self) -> None:
        self.square: Optional[ChessSquare] = None



class ChessGame:
    """
    object that represents one
    instance of a chess-game consisting
    of a board and rules.
    """

    def __init__(self) -> None:
        self.board: ChessBoard             = ChessBoard()
        self.rule_tree: list[ChessRule]    = [
            BoundsRule(self.board),
            PieceRule(self.board),
            AlliedPieceRule(self.board),
            KingRule(self.board),
            InCheckRule(self.board),
            ResolveCheckRule(self.board),
            ReachableRule(self.board, [
                StartingPawnRule(self.board)
            ])
        ]
        self.board.setup_default()
        

    def __switch_player__(self) -> None:
        self.player_to_move = not self.player_to_move


    def advance(self) -> None:
        for rule in self.rule_tree:
            rule.react()


    def resolve_source_square(self, mv: ChessMove):
        pass


    def is_legal(self, mv: ChessMove) -> bool:
        # if (not mv.get_source_square()):
        #     self.resolve_source_square(mv)
        for rule in self.rule_tree:
            if (rule.violated_by(mv)):
                return False
        return True
    

    def make_move(self, move: ChessMove) -> None:
        if (not self.is_legal(move)):
            raise InvalidMoveError(f"move '{move}' cannot be made in the current position")
        self.advance()
        self.board.apply_move(move)