
from gamelogic.piece import ChessPiece, ChessPieceType, ChessPieceColor
from gamelogic.square import ChessSquare
from gamelogic.board import ChessBoard

from typing import Callable, Optional

class ChessPieceMovePattern:
    """
    base-class for specifying how a chess-piece
    can move on the board.
    """

    def __init__(self,
                 sq_to_piece: Callable[[ChessSquare], Optional[ChessPiece]],
                 dimensions: tuple[int, int],
                 start_square: ChessSquare) -> None:
        self.start_square: ChessSquare   = start_square
        self.square_to_piece             = sq_to_piece
        self.squares: list[ChessSquare]  = list()
        self.__search__()

    
    def __blocked_by_ally__(self, sq: ChessSquare) -> bool:
        piece    = self.square_to_piece(self.start_square)
        sq_piece = self.square_to_piece(sq)
        if (sq_piece):
            return piece.get_color() == sq_piece.get_color()
        return False


    def __blocked_by_enemy__(self, sq: ChessSquare) -> bool:
        piece    = self.square_to_piece(self.start_square)
        sq_piece = self.square_to_piece(sq)
        if (sq_piece):
            return piece.get_color() != sq_piece.get_color()
        return False


    def __out_of_bounds__(self, sq: ChessSquare) -> bool:
        pass


    def __search__(self) -> None:
        """
        base-method to override.
        should perform the actual search of reachable squares.
        """
        self.squares.clear()
        if (not self.square_to_piece(self.start_square)):
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


    def get_piece(self) -> ChessPiece:
        pass


    def adjacents(self) -> None:
        for i in [ -1, 0, 1 ]:
            for j in [ -1, 0, 1 ]:
                if (i, j) != (0, 0):
                    self.squares.append(self.start_square + (i, j))


    def walk(self, dir: tuple[int, int]) -> None:
        """
        walks the board in the specified direction until
        a blocked or out-of-bounds square occurs.

        if the blocked square contains an allied piece, that square is not reachable,
        if it contains an enemy piece, the square is attackable and therefore
        contained in the result-list.
        """
        sq = self.start_square + dir
        while (not self.__out_of_bounds__(sq)):
            if (self.__blocked_by_enemy__(sq)):
                self.squares.append(sq)
                break
            elif (self.__blocked_by_ally__(sq)):
                break
            else:
                self.squares.append(sq)
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
        return self.squares



class ChessMove:
    """
    an object representing a move on a chess-board
    defined by a starting-square and an end-square.
    """


    def __init__(self,
                 source_square: ChessSquare,
                 target_square: ChessSquare) -> None:
        self.source_square: ChessSquare          = source_square
        self.target_square: ChessSquare          = target_square
        self.__validate__()


    def get_source_square(self) -> ChessSquare:
        """
        :returns: the square that contains the piece to be moved.
        """
        return self.source_square
    

    def get_target_square(self) -> ChessSquare:
        """
        :returns: the square to which the piece should be moved.
        """
        return self.target_square