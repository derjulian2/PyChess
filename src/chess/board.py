
from chess.common import ChessSquare, ChessColor, ChessPiece
from chess.bitboard import ChessBitBoard, ChessBitBoardPiece
from chess.navigator import ChessBoardNavigator
from chess.move import ChessMove, ChessMoveCastle, ChessMoveEnPassant, ChessMovePromotion, ChessCastleDescr

from typing import Optional


class ChessBoard(ChessBitBoard):
    """
    defines some more practical
    methods ontop of the ChessBitBoard.
    """

    def __init__(self) -> None:
        super().__init__()
        self.attacked_squares: dict[ChessColor, list[ChessSquare]] = dict()
        self.__gen_attacked_squares__()


    def __gen_attacked_squares__(self) -> None:
        for color in [ ChessColor.white, ChessColor.black]:
            res = list()
            for square, piece in self.get_pieces(color.invert()):
                nav = ChessBoardNavigator(self, square)
                match (piece.piece):
                    case (ChessPiece.pawn):
                        res += self.__gen_attack_squares_pawn__(nav)
                    case _:
                        res += self.gen_squares(square)
            self.attacked_squares[color] = res


    def __gen_push_squares_pawn__(self, nav: ChessBoardNavigator) -> list[ChessSquare]:
        res = list()
        push_1 = nav.advance()
        if (push_1):
            res.append(push_1)
            push_2 = nav.advance(2)
            if (push_2 and nav.__is_initial_pawn_rank__()):
                res.append(push_2)
        return res


    def __gen_attack_squares_pawn__(self, nav: ChessBoardNavigator) -> list[ChessSquare]:
        res = list()
        front = nav.__front__()
        for dx in [ 1, -1 ]:
            tmp = nav.relative(dx, front)
            if (tmp):
                res.append(tmp)
        return res


    def __gen_en_passant_squares_pawn__(self, nav: ChessBoardNavigator) -> list[ChessSquare]:
        res = list()
        for dx in [ 1, -1 ]:
            tmp = nav.relative(dx, 2 * nav.__front__())
            if (tmp):
                piece = self.get_square(tmp)[1]
                if (not piece.is_none() 
                    and piece.color != nav.__piece__().color 
                    and piece.piece == ChessPiece.pawn):
                    res.append(tmp)
        return res


    def __gen_squares_knight__(self, nav: ChessBoardNavigator) -> list[ChessSquare]:
        res = list()
        for dx, dy in [ (2, 1), (2, -1), (-2, 1), (-2, -1),
                        (1, 2), (1, -2), (-1, 2), (-1, -2) ]:
            tmp = nav.relative(dx, dy)
            if (tmp):
                res.append(tmp)
        return res


    def __gen_squares_king__(self, nav: ChessBoardNavigator) -> list[ChessSquare]:
        res = list()
        for dx in [ -1, 0, 1 ]:
            for dy in [ -1, 0, 1 ]:
                if (not (dx == 0 and dy == 0)):
                    tmp = nav.relative(dx, dy)
                    if (tmp):
                        res.append(tmp)
        return res


    def gen_squares(self, sq: ChessSquare) -> list[ChessSquare]:
        nav = ChessBoardNavigator(self, sq)
        squares = list()
        match (nav.__piece__().piece):
            case (ChessPiece.pawn):
                squares = self.__gen_push_squares_pawn__(nav)
                squares += [ 
                    atk_sq for atk_sq in self.__gen_attack_squares_pawn__(nav)
                    if nav.__is_blocked_by_enemy__(atk_sq)
                ]
            case (ChessPiece.knight):
                squares = self.__gen_squares_knight__(nav)
            case (ChessPiece.bishop):
                dirs = [ (1, 1), (-1, -1), (-1, 1), (1, -1) ]
                for dx, dy in dirs:
                    squares += nav.slide(dx, dy)
            case (ChessPiece.rook):
                dirs = [ (1, 0), (-1, 0), (0, 1), (0, -1) ]
                for dx, dy in dirs:
                    squares += nav.slide(dx, dy)
            case (ChessPiece.queen):
                dirs = [ (1, 0), (-1, 0), (0, 1), (0, -1), 
                         (1, 1), (-1, -1), (-1, 1), (1, -1) ]
                for dx, dy in dirs:
                    squares += nav.slide(dx, dy)
            case (ChessPiece.king):
                squares = self.__gen_squares_king__(nav)
        return squares
    

    def gen_moves(self, sq: ChessSquare) -> list[ChessMove]:
        return [ ChessMove(sq, tgt) for tgt in self.gen_squares(sq) ]


    def find_attacked_squares(self, color: ChessColor) -> list[ChessSquare]:
        return self.attacked_squares[color]


    def make_move(self, mv: ChessMove) -> None:
        src = self.get_square(mv.source)
        tgt = self.get_square(mv.target)

        if (isinstance(mv, ChessMoveCastle)):
            castle_squares = ChessMoveCastle.castle_to_squares[mv.descr()]
            self.set_square(castle_squares.king_target, src[1])
            self.set_square(src[0], ChessBitBoardPiece.none())
            self.set_square(castle_squares.rook_target, ChessBitBoardPiece(mv.color(), ChessPiece.rook))
            self.set_square(castle_squares.rook_source, ChessBitBoardPiece.none())
        elif (isinstance(mv, ChessMovePromotion)):
            self.set_square(tgt[0], ChessBitBoardPiece(src[1].color, mv.promotion))
            self.set_square(src[0], ChessBitBoardPiece.none())
        elif (isinstance(mv, ChessMoveEnPassant)):
            self.set_square(tgt[0], src[1])
            self.set_square(src[0], ChessBitBoardPiece.none())
            self.set_square(mv.en_passant, ChessBitBoardPiece.none())
        else:
            self.set_square(tgt[0], src[1])
            self.set_square(src[0], ChessBitBoardPiece.none())
        self.__gen_attacked_squares__()


    def is_attacked(self, sq: ChessSquare, color: ChessColor) -> bool:
        return sq in self.find_attacked_squares(color)


    def in_check(self, color: ChessColor) -> bool:
        kings = self.get_pieces(color, ChessPiece.king)
        for king in kings:
            if (self.is_attacked(king[0], king[1].color)):
                return True
        return False


    def can_castle(self, descr: ChessCastleDescr) -> bool:
        color, side = descr
        if (self.in_check(color)):
            return False
        
        kings = self.get_pieces(color, ChessPiece.king)
        if (len(kings) == 0):
            return False
        
        for square, piece in kings:
            if (color == ChessColor.white 
                and square != ChessSquare.from_str('e1')):
                return False
            elif (color == ChessColor.black 
                  and square != ChessSquare.from_str('e8')):
                return False
            
            nav = ChessBoardNavigator(self, square)
            squares_to_check = nav.castle(side)

            if (self.get_square(ChessMoveCastle.castle_to_squares[descr].rook_source)[1] 
                != ChessBitBoardPiece(color, ChessPiece.rook)):
                return False

            for sq in squares_to_check[1:-1]:
                if (not nav.__is_empty__(sq) 
                    or self.is_attacked(sq, color)):
                    return False
            
        return True