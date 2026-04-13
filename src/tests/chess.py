
from tests.unit_test import UnitTest, unit_test
from chess.square import ChessSquare
from chess.board import ChessBoard
from chess.piece import ChessColor, ChessPiece, ChessPieceType
from chess.move import ChessMove
from chess.game import ChessGame

from parsers.fen import FEN

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
        board = FEN.board_from_fen("8/8/8/6N1/8/2k1K3/8/8")
        board.is_in_check(ChessColor.black)

    @unit_test
    def game() -> None:
        pass
        # game = ChessGame()
        # game.make_move(ChessMove("e4"))
        # game.make_move(ChessMove("c6"))
        # game.make_move(ChessMove("Bb4"))