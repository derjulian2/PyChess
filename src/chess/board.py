
from chess.piece import ChessColor, ChessPieceType, ChessPiece
from chess.square import ChessSquare
from chess.move import ChessMove
from utility.vec import vec2i

from typing import Optional, TypeAlias
from dataclasses import dataclass, field


ChessSquareView: TypeAlias = tuple[ChessSquare, Optional[ChessPiece]]


@dataclass
class ChessBoard:
    """
    object that models the state of a regular chess-board.
    the default-value is a standard 8x8 chess-board with
    a starting-position setup.
    """

    pieces: dict[ChessSquare, ChessPiece] = field(default_factory=dict)
    dimensions: vec2i                     = field(default=vec2i(8, 8))


    def get_rank(self, rank: int) -> list[ChessSquareView]:
        """
        :returns: a list of length 'self.get_rank_count()'
                  of ChessSquare-objects with optionally a 
                  ChessPiece-object that represents if a piece
                  is standing on that square or not.
                  the list corresponds to all squares of that rank on the board.
        """
        if (not (1 <= rank <= self.get_rank_count())):
            raise ValueError(f"invalid rank-access: {i}")
        res = list()
        for i in range(1, self.get_file_count() + 1):
            sq = ChessSquare(i, rank)
            res.append((sq, self.get_piece(sq)))
        return res
    

    def get_file(self, file: int) -> list[ChessSquareView]:
        """
        :returns: a list of length 'self.get_file_count()'
                  of ChessSquare-objects with optionally a 
                  ChessPiece-object that represents if a piece
                  is standing on that square or not.
                  the list corresponds to all squares of that file on the board.
        """
        if (not (1 <= file <= self.get_file_count())):
            raise ValueError(f"invalid file-access: {i}")
        res = list()
        for i in range(1, self.get_rank_count() + 1):
            sq = ChessSquare(file, i)
            res.append((sq, self.get_piece(sq)))
        return res


    def __set_pawn_row__(self, color: ChessColor, row: int) -> None:
        """
        sets a row to only pawns.

        :param color: the color of the pawns.
        :param row:   the rank to set.
        """
        for i in range(self.get_file_count()):
            self.pieces[ChessSquare(i + 1, row)] = ChessPiece(ChessPieceType.pawn, color)


    def __set_back_row__(self, color: ChessColor, row: int) -> None:
        """
        sets a row of 8-pieces to
        the standard-chess rook-to-rook back-rank layout.

        :param color: the color of the pieces.
        :param row:   the rank to set.
        """
        back_row = [
                    ChessPieceType.rook,
                    ChessPieceType.knight,
                    ChessPieceType.bishop,
                    ChessPieceType.queen,
                    ChessPieceType.king,
                    ChessPieceType.bishop,
                    ChessPieceType.knight,
                    ChessPieceType.rook 
                   ]   
        for i in range(len(back_row)):
            self.pieces[ChessSquare(i + 1, row)] = ChessPiece(back_row[i], color)


    def setup_default(self) -> None:
        """
        clears the board and sets a 
        standard chess starting-position.
        """
        self.clear()
        self.__set_pawn_row__(ChessColor.white, self.get_initial_pawn_rank(ChessColor.white))
        self.__set_pawn_row__(ChessColor.black, self.get_initial_pawn_rank(ChessColor.black))
        self.__set_back_row__(ChessColor.white, 1)
        self.__set_back_row__(ChessColor.black, self.get_rank_count())


    def is_out_of_bounds(self, sq: ChessSquare) -> bool:
        """
        performs a bounds-check on the passed square
        
        :param sq: the square to be checked.
        """
        return (not (1 <= sq.get_file() <= self.get_file_count()) or
                not (1 <= sq.get_rank() <= self.get_rank_count()))


    def clear(self) -> None:
        """
        clears the entire board to just empty squares.
        """
        self.pieces.clear()


    def get_file_count(self) -> int:
        """
        :returns: the number of columns/files. default is 8.
        """
        return self.dimensions.x
        

    def get_rank_count(self) -> int:
        """
        :returns: the number of rows/ranks. default is 8.
        """
        return self.dimensions.y


    def get_initial_pawn_rank(self, color: ChessColor) -> int:
        if (color == ChessColor.white):
            return 2
        else:
            return self.get_rank_count() - 1


    def get_piece(self, sq: ChessSquare) -> Optional[ChessPiece]:
        """
        indexed and safe-guarded
        access to squares in column-row/file-rank format.
        
        making the parameter be of type ChessSquare allows
        ChessSquare.from_board('a1') to return the actual
        square corresponding to a1 here.
        
        :param sq: the square on the board to be queried.
        :returns:  the square on the board corresponding
                   to the passed square-instance.
        """
        return self.pieces.get(sq)


    def has_piece(self, sq: ChessSquare) -> bool:
        """
        :returns: True if the passed square has a piece standing on it.
        """
        return sq in self.pieces.keys()


    def get_pieces(self,
                   *,
                   color: Optional[ChessColor] = None,
                   type: Optional[ChessPieceType]   = None) -> list[ChessSquareView]:
        """
        access to all pieces on the board (optionially filtered).

        :param color: only include pieces of that color.
        :param type:  only include pieces of that type. 

        :returns: a list containing all squares with pieces that
                  are standing on the board (optionally satisfying color or type conditions).
        """
        res: list[tuple[ChessSquare, ChessPiece]] = [ (square, piece) for square, piece in self.pieces.items() ]
        if (color):
            res = list(filter(lambda elem: elem[1].get_color() == color, res))
        if (type):
            res = list(filter(lambda elem: elem[1].get_type() == type, res))
        return res


    def __is_takeable__(self, sq: ChessSquare, st: ChessSquare) -> bool:
        """
        :returns: True if 'sq' is takeable from the perspective of the piece standing on 'st'.
                  a square is takeable if it is either empty or has 
                  an opponent piece standing on it that is not the king.
        """
        assert self.has_piece(st)

        return ((not self.has_piece(sq)) or
                (self.has_piece(sq) and 
                 self.get_piece(sq).get_color() != self.get_piece(st).get_color() and 
                 self.get_piece(sq).get_type() != ChessPieceType.king))
               

    def __walk_until_blocked__(self, sq: ChessSquare, dir: vec2i) -> list[ChessSquare]:
        """
        :returns: a list of traversed squares (including the blocking square).
        """
        assert self.has_piece(sq)

        res  = list()
        iter = sq + dir
        while (not self.is_out_of_bounds(iter) and
               self.__is_takeable__(iter, sq)):
            res.append(iter)
            iter = iter + dir
        return res


    def __find_pawn_squares__(self, sq: ChessSquare) -> list[ChessSquare]:
        assert self.has_piece(sq)
        assert self.get_piece(sq).get_type() == ChessPieceType.pawn
        
        # en-passant cannot be inferred from a board's position, this
        # information must be stored in the game-logic.
        res = list()
        if (self.get_piece(sq).get_color() == ChessColor.white):
            front = (0, 1)
        else:
            front = (0, -1)
        # regular push
        move_sq = sq + front
        if (not (self.is_out_of_bounds(move_sq)) and 
            not (self.has_piece(move_sq))):
            res.append(move_sq)

        # attack-squares, only if opponent present
        attack_squares = [ move_sq + (-1, 0), move_sq + (1, 0) ]
        for tmp in attack_squares:
            if (not (self.is_out_of_bounds(tmp)) and
                    (self.__is_takeable__(tmp, sq))):
                res.append(tmp)

        return tmp
    

    def __find_knight_squares__(self, sq: ChessSquare) -> list[ChessSquare]:
        assert self.has_piece(sq)
        assert self.get_piece(sq).get_type() == ChessPieceType.knight
        
        directions = [ 
            ([ (2, 0), (-2, 0) ], [ (0, 1), (0, -1) ]), 
            ([ (0, 2), (0, -2) ], [ (1, 0), (-1, 0) ])
        ]
        res = list()
        for dir in directions:
            for dir1 in dir[0]:
                for dir2 in dir[1]:
                    tmp = sq + dir1 + dir2
                    if (not self.is_out_of_bounds(tmp) and
                            self.__is_takeable__(tmp, sq)):
                        res.append(tmp)
        return res


    def __find_bishop_squares__(self, sq: ChessSquare) -> list[ChessSquare]:
        assert self.has_piece(sq)
        assert self.get_piece(sq).get_type() == ChessPieceType.bishop
        
        directions = [ (1, 1), (-1, 1), (1, -1), (-1, -1) ]
        res = list()
        for dir in directions:
            res += self.__walk_until_blocked__(sq, dir)
        return res


    def __find_rook_squares__(self, sq: ChessSquare) -> list[ChessSquare]:
        assert self.has_piece(sq)
        assert self.get_piece(sq).get_type() == ChessPieceType.rook
        
        directions = [ (1, 0), (-1, 0), (0, 1), (0, -1) ]
        res = list()
        for dir in directions:
            res += self.__walk_until_blocked__(sq, dir)
        return res


    def __find_queen_squares__(self, sq: ChessSquare) -> list[ChessSquare]:
        assert self.has_piece(sq)
        assert self.get_piece(sq).get_type() == ChessPieceType.queen
        
        return self.__find_rook_squares__(sq) + self.__find_bishop_squares__(sq)


    def __find_king_squares__(self, sq: ChessSquare) -> list[ChessSquare]:
        assert self.has_piece(sq)
        assert self.get_piece(sq).get_type() == ChessPieceType.king

        # disregards the fact that the king
        # cannot take pieces that are themselves
        # backed by other pieces.
        #
        # this behaviour is prohibited
        # using a rule in the game-logic.
        res = list()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                tmp = sq + (dx, dy)
                if (not (dx != 0 and dy != 0) and
                    not self.is_out_of_bounds(tmp) and
                        self.__is_takeable__(tmp, sq)):
                    res.append(tmp)
        return res


    def find_takeable(self, sq: ChessSquare) -> list[ChessSquare]:
        """
        :returns: a list of all squares that can be reached
                  by the piece standing on 'sq' in a single move.
                  if there is no piece standing on 'sq', returns
                  an empty list.
                  
                  disregards en-passant for pawns.
                  disregards check for kings.
        """
        if (not self.has_piece(sq)):
            return list()
        match (self.get_piece(sq).get_type()):
            case (ChessPieceType.pawn):
                return self.__find_pawn_squares__(sq)
            case (ChessPieceType.knight):
                return self.__find_knight_squares__(sq)
            case (ChessPieceType.bishop):
                return self.__find_bishop_squares__(sq)
            case (ChessPieceType.rook):
                return self.__find_rook_squares__(sq)
            case (ChessPieceType.queen):
                return self.__find_queen_squares__(sq)
            case (ChessPieceType.king):
                return self.__find_king_squares__(sq)
            

    def is_attacked(self, color: ChessColor, sq: ChessSquare) -> bool:
        """
        :returns: True if the passed square is attacked from 'color's perspective,
                  meaning that a piece of the opponent's color can reach that square.
        """
        opponent_pieces = self.get_pieces(color=not color)
        for square, piece in opponent_pieces:
            if (sq in self.find_takeable(square)):
                return True
        return False
    

    def is_in_check(self, color: ChessColor) -> bool:
        """
        :returns: True if 'color's king is attacked.
        """
        kings = self.get_pieces(color=color, type=ChessPieceType.king)
        assert len(kings) == 1

        king_sq = kings[0][0]
        return self.is_attacked(color, king_sq)
    

    def apply_move(self, mv: ChessMove) -> None:
        """
        applies a move to the current position.
        disregards rules like check or en-passant.

        this method is only meant for executing a pre-validated move.
        """
        assert mv.get_source_square() is not None
        assert mv.get_target_square() is not None
        assert self.has_piece(mv.get_source_square())
        
        piece = self.pieces.pop(mv.get_source_square())
        self.pieces[mv.get_target_square()] = piece