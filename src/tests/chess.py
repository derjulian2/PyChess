
from tests.unit_test import UnitTest, unit_test
from gamelogic.square import ChessSquare


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
        pass


    @unit_test
    def game() -> None:
        pass