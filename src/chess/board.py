
from chess.piece import ChessColor, ChessPieceType, ChessPiece
from chess.square import ChessSquare
from chess.move import ChessMove

from utility.vec import vec2i, vec

from typing import Optional, TypeAlias, Generator, Callable


ChessBoardSquare: TypeAlias = tuple[ChessSquare, Optional[ChessPiece]]
"""
a square on the board with optionally a piece-object,
representing the possibility of a piece standing on that square.
"""


ChessPieceSquare: TypeAlias = tuple[ChessSquare, ChessPiece]
"""
a square on the board with a piece-object,
representing the guarantee of a piece standing on that square.
"""


ChessRank: TypeAlias = list[ChessBoardSquare]
ChessFile: TypeAlias = list[ChessBoardSquare]


class ChessBoard:
    """
    object that models the state of a regular chess-board.
    the default-value is an empty, standard 8x8 chess-board.
    """

    def __init__(self, dimensions: vec2i = vec2i(8, 8)) -> None:
        self.pieces: dict[ChessSquare, ChessPiece] = dict()
        self.dimensions: vec2i                     = dimensions


    def __set_pawn_row__(self, color: ChessColor, row: int) -> None:
        """
        sets a row to only pawns.

        :param color: the color of the pawns.
        :param row:   the rank to set.
        """
        for i in range(1, self.get_file_count() + 1):
            self.pieces[ChessSquare(i, row)] = ChessPiece(ChessPieceType.pawn, color)


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
        for i in range(1, len(back_row) + 1):
            self.pieces[ChessSquare(i, row)] = ChessPiece(back_row[i - 1], color)


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


    def get_rank(self, rank: int) -> ChessRank:
        """
        :param rank: the number of the rank to get.
        :returns: a list of length 'self.get_rank_count()'
                  of ChessSquare-objects with optionally a 
                  ChessPiece-object that represents if a piece
                  is standing on that square or not.
                  the list corresponds to all squares of that rank on the board.
        :raises ValueError: if rank is not between 1 and self.get_rank_count().
        """
        if (not (1 <= rank <= self.get_rank_count())):
            raise ValueError(f"invalid rank-access: {i}")
        
        res = list()
        for i in range(1, self.get_file_count() + 1):
            sq = ChessSquare(i, rank)
            res.append((sq, self.get_piece(sq)))
        return res
    

    def get_file(self, file: int) -> ChessFile:
        """
        :param file: the number of the file to get.
        :returns: a list of length 'self.get_file_count()'
                  of ChessSquare-objects with optionally a 
                  ChessPiece-object that represents if a piece
                  is standing on that square or not.
                  the list corresponds to all squares of that file on the board.
        :raises ValueError: if file is not between 1 and self.get_file_count().
        """
        if (not (1 <= file <= self.get_file_count())):
            raise ValueError(f"invalid file-access: {i}")
        
        res = list()
        for i in range(1, self.get_rank_count() + 1):
            sq = ChessSquare(file, i)
            res.append((sq, self.get_piece(sq)))
        return res


    def get_initial_pawn_rank_num(self, color: ChessColor) -> int:
        """
        returns the initial starting-rank of the pawn-row
        relative to the passed player's color.
        in regular chess, this is 2 for white and 7 for black.

        :param color: the color of the player that you want
                      to know the initial pawn rank of.
        :returns: an integer representing the rank that pawns
                  of the color 'color' normally start on.
        """
        if (color == ChessColor.white):
            return 2
        else:
            return self.get_rank_count() - 1


    def clear(self) -> None:
        """
        clears the entire board to just empty squares.
        """
        self.pieces.clear()


    def setup_default(self) -> None:
        """
        clears the board and sets a 
        standard chess starting-position.
        """
        self.clear()
        self.__set_pawn_row__(ChessColor.white, self.get_initial_pawn_rank_num(ChessColor.white))
        self.__set_pawn_row__(ChessColor.black, self.get_initial_pawn_rank_num(ChessColor.black))
        self.__set_back_row__(ChessColor.white, 1)
        self.__set_back_row__(ChessColor.black, self.get_rank_count())


    def is_out_of_bounds(self, sq: ChessSquare) -> bool:
        """
        performs a bounds-check on the passed square.
        
        :param sq: the square to be checked.
        :returns: True if the coordinates of the square are
                  outside of the size of the board.
        """
        return (not (1 <= sq.get_file() <= self.get_file_count()) or
                not (1 <= sq.get_rank() <= self.get_rank_count()))


    def get_piece(self, sq: ChessSquare) -> Optional[ChessPiece]:
        """
        query if a piece is standing on the passed square.

        :returns: a ChessPiece-object if a piece is standing
                  on the passed square, None otherwise.
        """
        return self.pieces.get(sq)


    def get_pieces(self,
                   *,
                   color: Optional[ChessColor] = None,
                   type: Optional[ChessPieceType]   = None) -> list[ChessPieceSquare]:
        """
        access to all pieces on the board (optionially filtered).

        :param color: only include pieces of that color.
        :param type:  only include pieces of that type. 

        :returns: a list containing all squares with pieces that
                  are standing on the board (optionally satisfying color or type conditions).
        """
        res: list[ChessPieceSquare] = [ (square, piece) for square, piece in self.pieces.items() ]
        if (color):
            res = list(filter(lambda elem: elem[1].get_color() == color, res))
        if (type):
            res = list(filter(lambda elem: elem[1].get_type() == type, res))
        return res
    
    
    def apply_move(self, mv: ChessMove) -> None:
        """
        applies a move to the current position.
        disregards any rules of chess. this method is only meant for executing a pre-validated move.
        """        
        piece = self.pieces.pop(mv.get_source_square())
        self.pieces[mv.get_target_square()] = piece



class ChessPieceMovePatterns:
    """
    collection of generator-methods that each return a
    list of squares that could potentially be
    reached from a piece standing on it.

    performs no checks if squares are out-of-bounds
    or blocked or takeable whatsoever. this is done
    directly by the board.

    patterns are documented with silly ascii-art for each method.
        .. indicates an empty square.
        {} indicates the starting-square.
        <> indicates attackable squares
        () indicates reachable squares
        [] indicates attackable or reachable squares.
    """

    class ChessPiecePattern:
        """
        base-class for every pattern providing
        common functionality.
        """

        def __init__(self, 
                     sq: ChessSquare, 
                     board: ChessBoard) -> None:
            self.sq: ChessSquare   = sq
            self.piece: ChessPiece = board.get_piece(sq)
            self.board: ChessBoard = board

            if (not self.piece):
                raise ValueError("cannot apply movement-pattern onto square without a piece")


        def is_blocked(self, sq: ChessSquare) -> bool:
            piece = self.board.get_piece(sq)
            return piece is not None


        def is_reachable(self, sq: ChessSquare) -> bool:
            return not self.board.is_out_of_bounds(sq) and not self.is_blocked(sq)


        def is_takeable(self, sq: ChessSquare) -> bool:
            if (self.board.is_out_of_bounds(sq)):
                return False
            if (self.is_blocked(sq)):
                return self.board.get_piece(sq).get_color() != self.piece.get_color()
            return False


        def walk(self, dir: vec2i) -> Generator[ChessSquare]:
            """
            generates squares until out-of-bounds or another piece is hit.
            """
            iter = self.sq + dir
            while (self.is_reachable(iter)):
                yield iter
                iter = iter + dir
                

        def pierce(self, dir: vec2i) -> Generator[ChessSquare]:
            """
            generates a single square with an opponent's piece standing on it,
            blocking the way in the passed direction, or nothing.
            """
            iter = self.sq + dir
            while (self.is_reachable(iter)):
                iter = iter + dir
            if (self.is_takeable(iter)):
                yield iter
            

        def reachable(self) -> Generator[ChessSquare]:
            """
            stub to override. should return a generator-expression of squares
            yielding all other squares that the piece can reach without 
            taking an opponents piece.
            """
            pass


        def takeable(self) -> Generator[ChessSquare]:
            """
            stub to override. should return a generator-expression of squares
            yielding all other squares that the piece can reach
            with taking an opponents piece.
            """
            pass

    
    class ChessPieceDirectionalPattern(ChessPiecePattern):

        def __init__(self, 
                     directions: list[vec2i],
                     sq: ChessSquare, 
                     board: ChessBoard) -> None:
            super().__init__(sq, board)
            self.directions: list[vec2i] = directions


        def reachable(self) -> Generator[ChessSquare]:
            for dir in self.directions:
                yield from self.walk(dir)


        def takeable(self) -> Generator[ChessSquare]:
            for dir in self.directions:
                yield from self.pierce(dir)



    class PawnPattern(ChessPiecePattern):
        """
        pawn-move-pattern:
        ..........
        ....()....      ^
        ..<>()<>..      |
        ....{}.... front upwards
        ..........
        """

        def front(self) -> vec2i:
            if (self.piece.get_color() == ChessColor.white):
                return vec2i(0, 1)
            else:
                return vec2i(0, -1)
            

        def reachable(self) -> Generator[ChessSquare]:
            push_1 = self.sq + self.front()
            push_2 = self.sq + 2 * self.front()
            if (self.is_reachable(push_1)):
                yield push_1
                if (self.sq.get_rank() == self.board.get_initial_pawn_rank_num(self.piece.get_color())
                    and self.is_reachable(push_2)):
                    yield push_2
            

        def takeable(self) -> Generator[ChessSquare]:
            take_1 = self.sq + self.front() + (1, 0)
            take_2 = self.sq + self.front() + (-1, 0)
            for take_sq in [ take_1, take_2 ]:
                if (self.is_takeable(take_sq)):
                    yield take_sq



    class BishopPattern(ChessPieceDirectionalPattern):
        """
        bishop-move-pattern:
        []......[]
        ..[]..[]..
        ....{}....
        ..[]..[]..
        []......[]
        """
        
        def __init__(self, sq: ChessSquare, board: ChessBoard):
            super().__init__([ (1, 1), (-1, 1), (1, -1), (-1, -1) ], sq, board)



    class KnightPattern(ChessPiecePattern):
        """
        knight-move-pattern:
        ..[]..[]..
        []......[]
        ....{}....
        []......[]
        ..[]..[]..
        """

        directions = [ 
            ([ (2, 0), (-2, 0) ], [ (0, 1), (0, -1) ]), 
            ([ (0, 2), (0, -2) ], [ (1, 0), (-1, 0) ])
        ]

        def reachable(self) -> Generator[ChessSquare]:
            for dir in self.directions:
                for dir1 in dir[0]:
                    for dir2 in dir[1]:
                        sq = self.sq + dir1 + dir2
                        if (self.is_reachable(sq)):
                            yield sq


        def takeable(self) -> Generator[ChessSquare]:
            for dir in self.directions:
                for dir1 in dir[0]:
                    for dir2 in dir[1]:
                        sq = self.sq + dir1 + dir2
                        if (self.is_takeable(sq)):
                            yield sq


    
    class RookPattern(ChessPieceDirectionalPattern):
        """
        rook-move-pattern:
        ....[]....
        ....[]....
        [][]{}[][]
        ....[]....
        ....[]....
        """

        def __init__(self, sq: ChessSquare, board: ChessBoard):
            super().__init__([ (1, 0), (-1, 0), (0, 1), (0, -1) ], sq, board)


    
    class QueenPattern(ChessPieceDirectionalPattern):
        """
        queen-move-pattern:
        []..[]..[]
        ..[][][]..
        [][]{}[][]
        ..[][][]..
        []..[]..[]
        """
        
        def __init__(self, sq: ChessSquare, board: ChessBoard):
            super().__init__([ (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1) ], sq, board)



    class KingPattern(ChessPiecePattern):
        """
        king-move-pattern:
        ..........
        ..[][][]..
        ..[]{}[]..
        ..[][][]..
        ..........
        """

        def reachable(self) -> Generator[ChessSquare]:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    sq = self.sq + (dx, dy)
                    if (not (dx == 0 and dy == 0)
                        and self.is_reachable(sq)):
                        yield sq


        def takeable(self) -> Generator[ChessSquare]:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    sq = self.sq + (dx, dy)
                    if (not (dx == 0 and dy == 0)
                        and self.is_takeable(sq)):
                        yield sq
                        
    

    @staticmethod
    def get_pattern(sq: ChessPieceType, board: ChessBoard) -> ChessPiecePattern:
        piece = board.get_piece(sq)
        if (not piece):
            raise ValueError("cannot apply movement-pattern to square without a piece")
        match (piece.get_type()):
            case (ChessPieceType.pawn):
                return ChessPieceMovePatterns.PawnPattern(sq, board)
            case (ChessPieceType.knight):
                return ChessPieceMovePatterns.KnightPattern(sq, board)
            case (ChessPieceType.bishop):
                return ChessPieceMovePatterns.BishopPattern(sq, board)
            case (ChessPieceType.rook):
                return ChessPieceMovePatterns.RookPattern(sq, board)
            case (ChessPieceType.queen):
                return ChessPieceMovePatterns.QueenPattern(sq, board)
            case (ChessPieceType.king):
                return ChessPieceMovePatterns.KingPattern(sq, board)
            


class ChessBoardInfo:
    """
    additional information-queries on the board
    using ChessMovePatterns.
    """

    @staticmethod
    def is_attacked(board: ChessBoard, color: ChessColor, sq: ChessSquare) -> bool:
        """
        :returns: True if the passed square is attacked from 'color's perspective,
                  meaning that a piece of the opponent's color could take that square in the next move.
        """
        opponent_pieces = board.get_pieces(color=not color)
        for square, piece in opponent_pieces:
            pattern = ChessPieceMovePatterns.get_pattern(square, board)
            if (sq in pattern.takeable()):
                return True
        return False
    

    @staticmethod
    def is_in_check(board: ChessBoard, color: ChessColor) -> bool:
        """
        :returns: True if 'color's king is attacked.
        """
        kings = board.get_pieces(color=color, type=ChessPieceType.king)
        if (len(kings) == 0):
            raise ValueError("no kings on the board")
        
        king_sq = kings[0][0]
        return ChessBoardInfo.is_attacked(board, color, king_sq)