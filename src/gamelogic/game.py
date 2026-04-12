
from gamelogic.piece  import ChessColor, ChessColor, ChessPieceType
from gamelogic.square import ChessSquare
from gamelogic.board  import ChessBoard
from gamelogic.move   import ChessMove, InvalidMoveError, ChessMoveCastle, ChessMovePromotion

from typing import Optional
from copy import copy


class ChessGameProgress:

    def __init__(self) -> None:
        pass

    
    def in_progress(self) -> bool:
        pass



class ChessGameCastlingRights:

    def __init__(self) -> None:
        pass



class ChessRule:
    """
    object that models a rule
    that has to be obeyed when
    making a move.
    """

    def __init__(self, board: ChessBoard) -> None:
        self.board: ChessBoard = board


    def violated_by(self, mv: ChessMove) -> bool:
        pass


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
        return mv.get_target_square() not in self.board.find_reachable_squares(mv.get_source_square())


class CastlingRule(ChessRule):

    pass


class PromotionRule(ChessRule):

    pass


class EnPassantRule(ChessRule):

    pass


class ChessGame:


    def __init__(self) -> None:
        self.state: ChessGameProgress      = ChessGameProgress()
        self.board: ChessBoard             = ChessBoard()
        self.rules: list[ChessRule]        = [
            BoundsRule(self.board),
            PieceRule(self.board),
            AlliedPieceRule(self.board),
            KingRule(self.board),
            InCheckRule(self.board),
            ResolveCheckRule(self.board)
        ]
        
        self.player_to_move: ChessColor               = ChessColor.white
        self.en_passant: Optional[ChessSquare]        = None
        self.castling_rights: ChessGameCastlingRights = ChessGameCastlingRights()
        

    def __switch_player__(self) -> None:
        self.player_to_move = not self.player_to_move


    def __update_game__(self) -> None:
        self.__switch_player__()


    def __validate_move__(self, mv: ChessMove) -> bool:
        for rule in self.rules:
            if (rule.violated_by(mv)):
                return False
        return True
    

    def make_move(self, move: ChessMove) -> None:
        if (not self.state.in_progress()):
            raise InvalidMoveError("game is finished. no further moves are possible.")
        if (not self.__validate_move__(move)):
            raise InvalidMoveError(f"move '{move}' cannot be made in the current position")
        self.__update_game__()
        self.board.apply_move(move)