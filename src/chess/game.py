
from chess.common import ChessCastleSide, ChessGameState
from chess.board import ChessBoard
from chess.move import ChessMove, ChessMoveCastle, InvalidMoveError
from chess.fen import FEN
from chess.rules import (ChessRule,
    PieceRule, PlayerToMoveRule, MoveRule, 
    CastleRule, EnPassantRule, CheckRule
) 

from typing import TypeVar


RuleType = TypeVar("RuleType")

class ChessGame:

    def __init__(self) -> None:
        self.board: ChessBoard      = FEN.board_from_fen(FEN.board_starting_position)
        self.rules: list[ChessRule] = [
            PieceRule(),
            PlayerToMoveRule(),
            MoveRule(),
            CastleRule(),
            EnPassantRule(),
            CheckRule()
        ]


    def get_rule(self, rule: type[RuleType]) -> RuleType:
        for r in self.rules:
            if (isinstance(r, rule)):
                return r
        raise ValueError(f"no such rule: '{rule}'")


    def validate(self, mv: ChessMove) -> None:
        for rule in self.rules:
            rule.validate(mv, self.board)


    def update(self, mv: ChessMove) -> None:
        for rule in self.rules:
            rule.update(mv, self.board)


    def gen_possible_moves(self) -> list[ChessMove]:
        res = list()
        # regular moves, checked with rules
        player_to_move_rule = self.get_rule(PlayerToMoveRule)
        color               = player_to_move_rule.color
        for square, piece in self.board.get_pieces(color):
            for mv in self.board.gen_moves(square):
                try:
                    self.validate(mv)
                    res.append(mv)
                except: continue
        
        # special move: castling
        castling_rule = self.get_rule(CastleRule)
        rights        = castling_rule.rights[color]
        if (rights != ChessCastleSide.none):
            for descr in [ (color, ChessCastleSide.kingside), (color, ChessCastleSide.queenside) ]:
                if (rights & descr[1]
                    and self.board.can_castle(descr)):
                    mv = ChessMoveCastle.from_descr(descr[0], descr[1])
                    try:
                        self.validate(mv)
                        res.append(mv)
                    except: pass
        
        # special move: en-passant
        en_passant_rule = self.get_rule(EnPassantRule)
        if (en_passant_rule.is_possible()):
            for mv in en_passant_rule.moves:
                try: 
                    self.validate(mv)
                    res.append(mv)
                except: continue
        
        return res

    
    def is_checkmate(self) -> bool:
        return len(self.gen_possible_moves()) == 0 and self.board.in_check()


    def make_move(self, mv: ChessMove) -> None:
        try:
            self.validate(mv)
            self.update(mv)
            self.board.make_move(mv)
        except Exception as e:
            raise InvalidMoveError(f"cannot play '{mv}' in this position: {e}")
        