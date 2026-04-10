
from typing import Self, Optional, Iterable

from utility.vec import vec2i
    
class ChessSquare(vec2i):
    """
    object that represents a valid chess-square
    on the board. 
    
    is convertible from column-major
    integer-pair to chess-notation and vice-versa.
    (e.g. (5, 4) -> 'e4'). values start at (1, 1).
    """


    def __init__(self, iterable: Optional[Iterable]):
        if (len(iterable) != 2):
            raise ValueError("chess-square consists of a file and rank-value")
        super().__init__(iterable)
    
    
    def get_column(self) -> int:
        """
        :returns: an integer indicating the 
                  column of the square (from white's perspective, left).
        """
        return self.x


    def get_row(self) -> int:
        """
        :returns: an integer indicating the 
                  row of the square (from white's perspective, down).
        """
        return self.y


    def to_board(self) -> str:
        """
        :returns: a string of length 2 encoding the square
                  denoted by (self.column, self.row) in board-coordinates
                  (from white's perspective, bottomleft).
                  examples: (5, 4) -> 'e4', (1, 1) -> 'a1'
        """
        return f"{chr(self.get_column() + (ord('a') - 1))}{self.get_row()}"


    @classmethod
    def from_board(cls, coords: str) -> Self:
        """
        :returns: a ChessSquare-Object resolved from a string of length
                  2 to a pair of integers corresponding to the column
                  and row of a square on the board.
                  (from white's perspective, bottomleft).
                  examples: (5, 4) -> 'e4', (1, 1) -> 'a1'
        """
        if (len(coords) != 2):
            raise ValueError(f"invalid length for board-coordinates: '{coords}'")
        if (not coords[0].isalpha() or not coords[1].isnumeric()):
            raise ValueError(f"invalid board-coordinates: '{coords}'")
        column = ord(coords[0].lower()) - (ord('a') - 1) # 'a' -> 97
        row    = int(coords[1])
        return cls(row, column)