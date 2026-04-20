
from chess.common import ChessPiece, ChessColor, ChessSquare
from chess.bitboard import ChessBitBoardPiece
from chess.board import ChessBoard


class FEN:

    board_starting_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"


    @staticmethod
    def piece_to_fen(piece: ChessBitBoardPiece) -> str:
        if (piece.color == ChessColor.none or piece.piece == ChessPiece.none):
            raise ValueError(f"cannot convert '{piece}' to fen")
        res = str()
        match (piece.piece):
            case (ChessPiece.pawn):
                res = "p"
            case (ChessPiece.knight):
                res = "n"
            case (ChessPiece.bishop):
                res = "b"
            case (ChessPiece.rook):
                res = "r"
            case (ChessPiece.queen):
                res = "q"
            case (ChessPiece.king):
                res = "k"
        if (piece.color == ChessColor.white):
            res = res.upper()
        return res


    @staticmethod
    def piece_from_fen(s: str) -> ChessBitBoardPiece:
        match (s.lower()):
            case ("p"):
                piece = ChessPiece.pawn
            case ("n"):
                piece = ChessPiece.knight
            case ("b"):
                piece = ChessPiece.bishop
            case ("r"):
                piece = ChessPiece.rook
            case ("q"):
                piece = ChessPiece.queen
            case ("k"):
                piece = ChessPiece.king
            case _:
                raise ValueError(f"cannot convert of fen '{s}'")
        if (s.islower()):
            color = ChessColor.black
        else:
            color = ChessColor.white
        return ChessBitBoardPiece(color, piece)


    @staticmethod
    def board_to_fen(board: ChessBoard) -> str:
        res = str()
        empty_sq_count = 0
        
        def flush_if() -> None:
            nonlocal res, empty_sq_count
            if (empty_sq_count != 0):
                res += str(empty_sq_count)
                empty_sq_count = 0

        def handle_rank(rank_num: int) -> None:
            nonlocal res, empty_sq_count
            rank = board.get_rank(rank_num)
            for sq, piece in rank:
                if not (piece.is_none()):
                    flush_if()
                    res += FEN.piece_to_fen(piece)
                else:
                    empty_sq_count += 1
            flush_if()

        for i in reversed(range(2, 9)):
            handle_rank(i)
            res += "/"
        handle_rank(1)

        return res


    @staticmethod
    def board_from_fen(s: str) -> ChessBoard:
        res   = ChessBoard()
        ranks = s.split('/')
        
        if (len(ranks) != 8):
            raise ValueError(f"cannot resolve board from string: '{s}'")

        for i in range(len(ranks)):
            rank = ranks[i]
            file = 1
            for char in rank:
                if (char in "pnbrqkPNBRQK"):
                    res.set_square(ChessSquare(file, 8 - i), FEN.piece_from_fen(char))
                    file += 1
                elif (char.isdigit()):
                    file += int(char)
                else:
                    raise ValueError(f"cannot resolve board from string: '{s}'")
        return res
