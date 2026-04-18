
from tests.unit_test import UnitTest, unit_test
from chess.square import ChessSquare
from chess.board import ChessBoard, ChessPieceMovePatterns, ChessBoardInfo
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
        board = FEN.board_from_fen("8/4N3/8/3K2k1/8/8/3r4/8")

        print(ChessBoardInfo.is_in_check(board, ChessColor.black))
        print(ChessBoardInfo.is_in_check(board, ChessColor.white))

    @unit_test
    def game() -> None:
        pass
        # game = ChessGame()
        # game.make_move(ChessMove(ChessSquare("e2"), ChessSquare("e4")))
        # game.make_move(ChessMove(ChessSquare("e7"), ChessSquare("e5")))
        # game.make_move(ChessMove(ChessSquare("d1"), ChessSquare("h5")))
        # game.make_move(ChessMove(ChessSquare("b8"), ChessSquare("c6")))
        # game.make_move(ChessMove(ChessSquare("f1"), ChessSquare("c4")))
        # game.make_move(ChessMove(ChessSquare("g8"), ChessSquare("f6")))
        # game.make_move(ChessMove(ChessSquare("h5"), ChessSquare("f7")))
        # game.make_move(ChessMove(ChessSquare("e8"), ChessSquare("e7")))