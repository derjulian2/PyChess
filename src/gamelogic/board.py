
from gamelogic.piece import ChessColor, ChessPieceType, ChessPiece
from gamelogic.square import ChessSquare
from gamelogic.move import ChessMove

from typing import Optional
from __future__ import annotations
from utility.vec import vec2i


class ChessBoard:
    """
    object that models the state of a regular chess-board.
    the default-value is a standard 8x8 chess-board with
    a starting-position setup.
    """


    def __init__(self,
                 dimensions: vec2i = vec2i((8, 8))) -> None:
        self.pieces: dict[ChessSquare, ChessPiece] = dict()
        self.dimensions: vec2i = dimensions
        self.__set_starting_position__()
    

    def __set_pawn_row__(self, color: ChessColor, row: int) -> None:
        """
        sets a row to only pawns.

        :param color: the color of the pawns.
        :param row:   the rank to set.
        """
        for i in range(self.get_width()):
            self.pieces[ChessSquare((i, row))] = ChessPiece(ChessPieceType.pawn, color)


    def __set_back_row__(self, color: ChessColor, row: int) -> None:
        """
        sets a row of 8-pieces to
        the standard-chess rook-to-rook back-rank layout.

        :param color: the color of the pieces.
        :param row:   the rank to set.
        """
        back_row = [
                ChessPiece(ChessPieceType.rook, color),
                ChessPiece(ChessPieceType.knight, color),
                ChessPiece(ChessPieceType.bishop, color),
                ChessPiece(ChessPieceType.queen, color),
                ChessPiece(ChessPieceType.king, color),
                ChessPiece(ChessPieceType.bishop, color),
                ChessPiece(ChessPieceType.knight, color),
                ChessPiece(ChessPieceType.rook, color)
        ]
        for i in range(len(back_row)):
            self.pieces[ChessSquare((i, row))] = back_row[i]


    def __set_starting_position__(self) -> None:
        """
        clears the board and sets a 
        standard chess starting-position.
        """
        self.clear()
        self.__set_pawn_row__(ChessColor.white, 2)
        self.__set_pawn_row__(ChessColor.black, 7)
        self.__set_back_row__(ChessColor.white, 1)
        self.__set_back_row__(ChessColor.black, 8)


    def __out_of_bounds__(self, sq: ChessSquare) -> bool:
        """
        performs a bounds-check on the passed square
        
        :param sq: the square to be checked.
        """
        if (sq.get_file() <= 0               or sq.get_rank() <= 0 or
            sq.get_file() > self.get_width() or sq.get_rank() > self.get_height()):
            return True
        return False
    

    def __move_plausible__(self, mv: ChessMove) -> bool:
        """
        :returns: True if the passed move is 'plausible', meaning
                  that it doesn't violate basic chess-rules. this does not
                  take special rules (like check or en-passant) into account.
        :param mv: the move to be checked.
        """
        # bounds-check
        if (self.__out_of_bounds__(mv.get_source_square()) or
            self.__out_of_bounds__(mv.get_target_square())):
            return False
        
        # no piece on source-square
        if (not self.square_has_piece(mv.get_source_square())):
            return False
        
        if (self.square_has_piece(mv.get_target_square())):
            src_piece = self.get_piece(mv.get_source_square())
            tgt_piece = self.get_piece(mv.get_target_square())

            # taking an allied piece
            if (src_piece.get_color() == tgt_piece.get_color()):
                return False
            
            # taking a king-piece
            if (tgt_piece.get_type() == ChessPieceType.king):
                return False
            
        return True


    def clear(self) -> None:
        """
        clears the entire board to just empty squares.
        """
        self.pieces.clear()


    def get_width(self) -> int:
        """
        :returns: the number of columns/files. default is 8.
        """
        return self.dimensions.x
    

    def get_height(self) -> int:
        """
        :returns: the number of rows/ranks. default is 8.
        """
        return self.dimensions.y


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
        if (self.__out_of_bounds__(sq)):
            raise ValueError("tried to get piece from out-of-bounds square")
        return self.pieces.get(sq)


    def square_has_piece(self, sq: ChessSquare) -> bool:
        """
        :returns: True if the passed square has a piece standing on it.
        """
        return sq in self.pieces.keys()


    def get_pieces(self,
                   *,
                   color: Optional[ChessColor] = None,
                   type: Optional[ChessPieceType]   = None) -> list[tuple[ChessSquare, ChessPiece]]:
        """
        access to all pieces on the board (optionially filtered).

        :param color: only include pieces of that color.
        :param type:  only include pieces of that type. 

        :returns: a list containing all squares with pieces that
                  are standing on the board (optionally satisfying color or type conditions).
        """
        res: list[tuple[ChessSquare, ChessPiece]] = [ (square, piece) for square, piece in self.pieces.values() ]
        if (color):
            res = list(filter(lambda elem: elem[1].get_color() == color, res))
        if (type):
            res = list(filter(lambda elem: elem[1].get_type() == type, res))
        return res
    
    
        pieces = self.get_pieces(color=color, type=ChessPieceType.king)
        if (len(pieces) == 0):
            return None
        return pieces[0]


    def apply_move(self, move: ChessMove) -> None:
        if (not self.__move_plausible__(move)):
            return


    class Navigator:
        """
        class to determine the reachable
        squares from a single square on the board.

        disregards special moves like en-passant or castling.
        """

        def __init__(self,
                    board: ChessBoard,
                    start_square: ChessSquare) -> None:
            self.start_square: ChessSquare   = start_square
            self.board: ChessBoard           = board

            self.reachable_squares: list[ChessSquare]  = list()
            self.attackable_squares: list[ChessSquare] = list()
            self.__find_squares__()

        
        def __blocked_by_ally__(self, sq: ChessSquare) -> bool:
            piece    = self.board.get_piece(self.start_square)
            sq_piece = self.board.get_piece(sq)
            if (sq_piece):
                return piece.get_color() == sq_piece.get_color()
            return False


        def __front__(self) -> vec2i:
            piece = self.board.get_piece(self.start_square)
            if (piece.get_color() == ChessColor.black):
                return vec2i((0, -1))
            else:
                return vec2i((0, 1))


        def __blocked_by_enemy__(self, sq: ChessSquare) -> bool:
            piece    = self.board.get_piece(self.start_square)
            sq_piece = self.board.get_piece(sq)
            if (sq_piece):
                return piece.get_color() != sq_piece.get_color()
            return False


        def __out_of_bounds__(self, sq: ChessSquare) -> bool:
            return self.board.__out_of_bounds__(sq)


        def __pawn_squares__(self) -> None:
            self.__append_square_if__(self.start_square + self.__front__() + (1, 0))
            self.__append_square_if__(self.start_square + self.__front__() + (-1, 0))


        def __find_squares__(self) -> None:
            """
            should perform the actual search of reachable squares.
            """
            self.reachable_squares.clear()
            self.attackable_squares.clear()
            if (not self.board.get_piece(self.start_square)):
                return
            match (self.get_piece().get_type()):
                case (ChessPieceType.pawn):
                    pass
                case (ChessPieceType.knight):
                    pass
                case (ChessPieceType.bishop):
                    self.diagonals()
                case (ChessPieceType.rook):
                    self.straights()
                case (ChessPieceType.queen):
                    self.diagonals()
                    self.straights()
                case (ChessPieceType.king):
                    self.adjacents()


        def __append_square_if__(self, sq: ChessSquare) -> bool:
            piece = self.board.get_piece(sq)
            if (piece):
                if (self.__blocked_by_enemy__(sq)):
                    self.attackable_squares.append(sq)
                return False
            else:
                self.reachable_squares.append(sq)
                return True


        def get_piece(self) -> ChessPiece:
            if (not self.board.square_has_piece(self.start_square)):
                raise ValueError("no piece where there should be one")
            return self.board.get_piece(self.start_square)


        def adjacents(self) -> None:
            for i in [ -1, 0, 1 ]:
                for j in [ -1, 0, 1 ]:
                    if (i, j) != (0, 0):
                        self.__append_square_if__(self.start_square + (i, j))


        def walk(self, dir: vec2i) -> None:
            """
            walks the board in the specified direction until
            a blocked or out-of-bounds square occurs.

            if the blocked square contains an allied piece, that square is not reachable,
            if it contains an enemy piece, the square is attackable and therefore
            contained in the result-list.
            """
            sq = self.start_square + dir
            while (not self.__out_of_bounds__(sq) 
                and self.__append_square_if__(sq)):
                sq = sq + dir
        

        def straights(self) -> None:
            """
            walks straight into all 4 directions.
            """
            directions = [ (1, 0), (-1, 0), (0, 1), (0, -1) ]
            for dir in directions:
                self.walk(dir)


        def diagonals(self) -> list[ChessSquare]:
            """
            walks diagonal into all 4 directions.
            """
            directions = [ (1, 1), (-1, 1), (1, -1), (-1, -1) ]
            for dir in directions:
                self.walk(dir)
                

        def get_reachable_squares(self) -> list[ChessSquare]:
            """
            :returns: a list of reachable squares from the piece contained in the starting square.
            """
            return self.reachable_squares
        
        
        def get_attackable_squares(self) -> list[ChessSquare]:
            return self.attackable_squares
        

        def get_all_squares(self) -> list[ChessSquare]:
            return self.reachable_squares + self.attackable_squares