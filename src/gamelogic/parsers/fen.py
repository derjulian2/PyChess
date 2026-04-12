
class FENPatterns:

    rank             = r"[1-8]"
    file             = r"[a-h]"
    square           = rf"{file}{rank}"
    integer          = r"[0-9]+"
    blank            = r"[\s]+"
    none             = r"[-]"
    
    to_move         = r"[wb]"
    castling_rights = rf"K?Q?k?q?|{none}"
    en_passant      = rf"{square}|{none}"
    row             = r"[PNBRQKpnbrqk1-8]+"
    board           = rf"(?:{row}/)" + r"{7}" + row

    fen  = (rf"^(?P<board>{board})"
            + rf"{blank}(?P<to_move>{to_move})"
            + rf"{blank}(?P<castling_rights>{castling_rights})"
            + rf"{blank}(?P<en_passant>{en_passant})"
            + rf"{blank}(?P<half_moves>{integer})"
            + rf"{blank}(?P<moves>{integer})$")


from gamelogic.piece import ChessPieceType, ChessPiece, ChessColor
from gamelogic.square import ChessSquare
from gamelogic.board import ChessBoard


class FEN:
    """
    conversions from the here
    implemented chess-types to FEN-notation.

    https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
    """

    @staticmethod
    def piece_to_fen(piece: ChessPiece) -> str:
        """
        :returns: a single character encoding a chess-piece.
                  lowercase for black, uppercase for white.
        """
        res: str
        match (piece.get_type()):
            case (ChessPieceType.pawn):
                res = "P"
            case (ChessPieceType.knight):
                res = "N"
            case (ChessPieceType.bishop):
                res = "B"
            case (ChessPieceType.rook):
                res = "R"
            case (ChessPieceType.queen):
                res = "Q"
            case (ChessPieceType.king):
                res = "K"
        if (piece.get_color() == ChessColor.black):
            res = res.lower()
        return res
    

    @staticmethod
    def board_to_fen(board: ChessBoard) -> str:
        """
        :returns: a string encoding an entire
                  position on the chess-board.
        """
        res = str()
        empty_sq_count = 0
        
        def flush_if() -> None:
            nonlocal res, empty_sq_count
            if (empty_sq_count != 0):
                res += str(empty_sq_count)
                empty_sq_count = 0

        def handle_rank(rank: int) -> None:
            nonlocal res, empty_sq_count
            rank = board.get_rank(i)
            for sq, piece in rank:
                if (piece):
                    flush_if()
                    res += FEN.piece_to_fen(piece)
                else:
                    empty_sq_count += 1
            flush_if()

        for i in reversed(range(2, board.get_rank_count() + 1)):
            handle_rank(i)
            res += "/"
        handle_rank(1)

        return res


    @staticmethod
    def to_fen(obj: ChessPiece | ChessBoard) -> str:
        """
        dispatch-method for simple interface.
        calls the corresponding FEN.<...>_to_fen() method
        based on the parameter-type.

        :param obj: the chess-object to convert to a FEN-string.
        """
        match (obj):
            case (ChessPiece()):
                return FEN.piece_to_fen(obj)
            case (ChessBoard()):
                return FEN.board_to_fen(obj)
        raise TypeError("unsupported type for FEN-conversion")


    @staticmethod
    def piece_from_fen(s: str) -> ChessPiece:
        assert len(s) == 1
        assert s.lower() in "pnbrqk"

        if (s.isupper()):
            color = ChessColor.white
        else:
            color = ChessColor.black

        match (s.lower()):
            case ("p"):
                type = ChessPieceType.pawn
            case ("n"):
                type = ChessPieceType.knight
            case ("b"):
                type = ChessPieceType.bishop
            case ("r"):
                type = ChessPieceType.rook
            case ("q"):
                type = ChessPieceType.queen
            case ("k"):
                type = ChessPieceType.king
        
        return ChessPiece(type, color)


    @staticmethod
    def board_from_fen(s: str) -> ChessBoard:
        res = ChessBoard()
        res.clear()

        ranks = s.split("/")
        assert len(ranks) == res.get_rank_count()
        
        for i in range(len(ranks)):
            rank = ranks[i]
            file = 1
            for char in rank:
                if (char in "pnbrqkPNBRQK"):
                    res.pieces[ChessSquare(file, res.get_rank_count() - i)] = FEN.piece_from_fen(char)
                    file += 1
                elif (char.isdigit()):
                    file += int(char)
                else:
                    assert False
        return res


    # @staticmethod
    # def from_fen(s: str) -> ChessPiece | ChessBoard:
    #     """
    #     dispatch-method for simple interface.
    #     calls the corresponding FEN.<...>_from_fen() method
    #     based on the parameter-type.

    #     :param obj: the chess-object to construct from a FEN-string (or sections of it).
    #     """
    #     match ():
    #         case (ChessPiece()):
    #             return FEN.piece_to_fen(obj)
    #         case (ChessBoard()):
    #             return FEN.board_to_fen(obj)
    #     raise TypeError("unsupported type for FEN-conversion")