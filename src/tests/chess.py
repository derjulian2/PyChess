
from tests.unit_test import UnitTest, unit_test
from gamelogic.square import ChessSquare
from gamelogic.board import ChessBoard
from gamelogic.piece import ChessColor, ChessPiece, ChessPieceType

from gamelogic.parsers.fen import FEN

class ChessTests:
    """
    unit-tests for the chess-backend.
    """


    @unit_test
    def square() -> None:
        a = ChessSquare("a1")
        b = ChessSquare("e4")
        c = ChessSquare(5, 4)
        d = ChessSquare((8, 8))
        e = ChessSquare("a1") + (1, 1)


        UnitTest.assert_eq(str(a), "a1")
        UnitTest.assert_eq(b, (5, 4))
        UnitTest.assert_eq(str(c), "e4")
        UnitTest.assert_eq(str(d), "h8")
        UnitTest.assert_eq(str(e), "b2")
        

    @unit_test
    def board() -> None:
        b = FEN.board_from_fen("8/8/8/6N1/8/2k1K3/8/8")
        b.is_in_check(ChessColor.black)

    @unit_test
    def game() -> None:
        pass