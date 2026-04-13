
from chess.piece  import ChessColor, ChessColor, ChessPieceType, ChessPiece
from chess.square import ChessSquare
from chess.board  import ChessBoard
from chess.move   import ChessMove, InvalidMoveError, ChessMoveCastle, ChessMovePromotion, ChessCastleSide

from typing import Optional, Self
from copy import copy
from dataclasses import dataclass, field
from parsers.fen import FEN


@dataclass
class ChessRule:
    """
    object that models a rule
    that has to be obeyed when
    making a move.

    rules can be somewhat dependent on each other
    (for example a move is OK if the piece that was
     moved is now on a reachable square OR if a special move was played
     (like en-passant or castling)).

    this behaviour is handled explicitly in ChessGame.__evaluate_rules__
    """

    board: ChessBoard


    def violated_by(self, mv: ChessMove) -> bool:
        """
        stub to override. should return True
        if the passed move is not permitted by 
        the behaviour of the rule.
        """
        pass


    def update(self, mv: ChessMove) -> None:
        """
        stub to override. should adjust the internal
        rule-state to the played move.        
        """
        pass



@dataclass
class PlayerToMoveRule(ChessRule):
    """
    moving a piece that is not
    the current-player's color is disallowed.
    """

    player_to_move: ChessColor = ChessColor.white


    def violated_by(self, mv: ChessMove) -> bool:
        piece = self.board.get_piece(mv.get_source_square())
        return piece.get_color() != self.player_to_move


    def update(self, mv: ChessMove) -> None:
        self.player_to_move = self.player_to_move.invert()



class BoundsRule(ChessRule):
    """
    a move cannot start or end
    out-of-bounds.
    """

    def violated_by(self, mv: ChessMove) -> bool:
        return (self.board.is_out_of_bounds(mv.get_source_square()) or
                self.board.is_out_of_bounds(mv.get_target_square()))
    


class EmptySquareRule(ChessRule):
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
        return False # no piece to take, always pass
        


class KingTakeRule(ChessRule):
    """
    a move cannot take a king-piece.
    """

    def violated_by(self, mv: ChessMove) -> bool:
        if (self.board.has_piece(mv.get_target_square())):
            src_piece = self.board.get_piece(mv.get_source_square())
            tgt_piece = self.board.get_piece(mv.get_target_square())
            return tgt_piece.get_type() == ChessPieceType.king
        return False # no piece to take, always pass



class WouldBeInCheckRule(ChessRule):
    """
    the king cannot move
    to a square that would result in
    him being takeable in the next move.
    """

    def violated_by(self, mv: ChessMove) -> bool:
        src_piece = self.board.get_piece(mv.get_source_square())
        if (src_piece.get_type() == ChessPieceType.king):
            return self.board.is_attacked(src_piece.get_color(), mv.get_target_square())
        return False # no king move, does not concern this rule



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
        return False # not in check, does not concern this rule



class CheckMateRule(ChessRule):
    """
    if a player is in check, and there is no
    move that would resolve that check left for him,
    then it is checkmate and the game is over.
    """

    def violated_by(self, mv: ChessMove) -> bool:
        return False



class PawnTakeRule(ChessRule):
    """
    a pawn can only move diagonally
    if there is a piece on the target-square.
    """

    def violated_by(self, mv: ChessMove) -> bool:
        piece = self.board.get_piece(mv.get_source_square())
        if (piece.get_type() == ChessPieceType.pawn):
            delta: ChessSquare = abs(mv.get_source_square() - mv.get_target_square())
            if (delta == (1, 1)): # diagonal, must be a take
                return not self.board.has_piece(mv.get_target_square())
        return False # not a pawn-move, does not concern this rule



class RegularMoveRule(ChessRule):
    """
    a regular move must obey
    the movement-patterns implemented in
    ChessBoard.__find_<piece_type>_squares__ corresponding to the piece
    currently standing on that square.
    """
    
    def violated_by(self, mv: ChessMove) -> bool:
        return (mv.get_target_square() not in self.board.find_takeable(mv.get_source_square()) and
                mv.get_target_square() not in self.board.find_reachable(mv.get_source_square()))



@dataclass
class CastlingRule(ChessRule):
    """
    a castling-move is only valid
    if the player still has the rights to
    do so and only if the involved squares are
    not attacked by any opponent-piece.
    """


    rights: dict[ChessColor, ChessCastleSide] = field(default_factory=lambda: { 
        color : ChessCastleSide.kingside | ChessCastleSide.queenside for color in ChessColor
    })


    def violated_by(self, mv: ChessMoveCastle) -> bool:
        if (not isinstance(mv, ChessMoveCastle)):
            return False
        
        if (mv.get_side() & ChessCastleSide.kingside and mv.get_side() & ChessCastleSide.queenside):
            return True # cannot castle to both sides at once
        
        piece = self.board.get_piece(mv.get_source_square())
        if (piece.get_type() != ChessPieceType.king):
            return True # source-square must contain king
        
        # squares up until the rook must not be attacked or blocked
        if (mv.get_side() == ChessCastleSide.kingside):
            dir = ()
        else:
            dir = ()
        squares = self.board.walk_until_blocked(mv.get_source_square(), dir)
        if (mv.get_side() == ChessCastleSide.kingside and len(squares) != 3):
            return True
        elif (mv.get_side() == ChessCastleSide.queenside and len(squares) != 4):
            return True
        for sq in squares:
            if (self.board.is_attacked(piece.get_color(), sq)):
                return True
            elif (self.board.has_piece(sq)):
                return True
            
        if (not self.rights[piece.get_color()] & mv.get_side()):
            return True # does not have the right to castle.
                        # 
                        # you don't have the right, O' you don't have the right,
                        # all the more, O' you don't have the right
        return False


    def update(self, mv: ChessMoveCastle):
        if (not isinstance(mv, ChessMoveCastle)):
            return
        
        piece = self.board.get_piece(mv.get_source_square())
        self.rights[piece.get_color()] &= ~mv.get_side()



class PromotionRule(ChessRule):
    """
    promotion should only be valid for
    pawn-moves from the second-last to the
    last rank.
    only promotion to a everything but a king or pawn is allowed.
    """


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
        

    def update(self, mv: ChessMovePromotion) -> None:
        if not (isinstance(mv, ChessMovePromotion)):
            return
        
        piece = self.board.get_piece(mv.get_source_square())
        self.board.pieces[mv.get_target_square()] = ChessPiece(mv.get_promotion(), piece.get_color())



@dataclass
class EnPassantRule(ChessRule):
    """
    a pawn can take another pawn 'en-passant'
    if it is standing next to it, but only
    in the first move just after the pawn to be taken
    has passed the other pawn with a double-push.
    """

    square: Optional[ChessSquare] = None


    def violated_by(self, mv: ChessMove) -> bool:
        return False


    def update(self, mv: ChessMove) -> None:
        piece = self.board.get_piece(mv.get_source_square())
        if (piece.get_type() == ChessPieceType.pawn):
            delta: ChessSquare = abs(mv.get_source_square() - mv.get_target_square())
            if (delta == (0, 2)): # double-push, candidate for en-passant
                pass



class ChessGame:
    """
    object that represents one
    instance of a chess-game consisting
    of a board and rules.
    """

    def __init__(self) -> None:
        self.board: ChessBoard = ChessBoard()
       
        self.meta_rules: list[ChessRule] = [
            # meta-rules (turn-order)
            PlayerToMoveRule(self.board)
        ]

        self.move_validation_rules: list[ChessRule] = [
            # basic move-validation rules
            BoundsRule(self.board),
            EmptySquareRule(self.board),
            AlliedPieceRule(self.board),
            KingTakeRule(self.board),
            PromotionRule(self.board)
        ]

        self.movement_rules: list[ChessRule] = [
            # movement-rules
            RegularMoveRule(self.board),
            PawnTakeRule(self.board),
            CastlingRule(self.board),
            EnPassantRule(self.board)
        ]

        self.check_rules: list[ChessRule] = [
            # check-rules
            WouldBeInCheckRule(self.board),
            ResolveCheckRule(self.board),
            CheckMateRule(self.board)
        ]

        self.board.setup_default()
        

    def __get_all_rules__(self) -> list[ChessRule]:
        return (self.meta_rules
                + self.move_validation_rules
                + self.movement_rules
                + self.check_rules)


    def __get_rule__(self, rule_type: type) -> ChessRule:
        return { type(rule) : rule for rule in self.__get_all_rules__() }[rule_type]


    def __violates_rules__(self, mv: ChessMove) -> Optional[type]:
        """
        evaluates every rule in self.rules with a passed
        move and applies some hardcoded logic to finally
        determine if a move can be played or not.

        :returns: the rule that was violated.
        """
        for rule in self.__get_all_rules__():
            if (rule.violated_by(mv)):
                return type(rule)
        
        return None


    def advance(self, move: ChessMove) -> None:
        """
        advances the game-logic according to the played move
        (e.g. updates castling-rights or en-passant-state).
        """
        for rule in self.__get_all_rules__():
            rule.update(move)


    def resolve_source_square(self, mv: ChessMove):
        pass


    def is_legal(self, move: ChessMove) -> bool:
        """
        :returns: True if the chess-move encoded in 'move'
                  is valid to play according to the rules 
                  evaluated in self.__evaluate_rules__ .
        """
        if (not move.get_source_square()):
            self.resolve_source_square(move)
        rule = self.__violates_rules__(move)
        if (rule):
            print(f"violated rule: {rule}")
        return rule is None


    def make_move(self, move: ChessMove) -> None:
        """
        checks if 'move' is legal to play in the current position,
        advances the game-logic and applies the move to the board if
        everything is fine.

        :raises InvalidMoveError: if 'move' violates the rules according to the
                                  logic in ChessGame.__evaluate_rules__ .
        """
        if (not self.is_legal(move)):
            raise InvalidMoveError(f"move '{move}' cannot be made in the current position")
        self.advance(move)
        self.board.apply_move(move)