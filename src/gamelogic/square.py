
from utility.vec import vec2i

from typing import Self, Optional, Iterable


class ChessSquare(vec2i):
    """
    object that represents a valid chess-square
    on the board. 
    
    convertible from file-major
    integer-pair to chess-notation and vice-versa.
    (e.g. (5, 4) -> 'e4').
    """


    def __init__(self, *args):
        if (len(args) == 1 and isinstance(args[0], str)):
            super().__init__(0, 0)
            self.from_board(args[0])
        else:
            super().__init__(*args)
        

    
    def __str__(self) -> str:
        """
        string conversion. always to board-coordinates.
        """
        return self.to_board()


    def get_file(self) -> int:
        """
        :returns: an integer indicating the 
                  file of the square (from white's perspective, left).
        """
        return self.x


    def get_rank(self) -> int:
        """
        :returns: an integer indicating the 
                  rank of the square (from white's perspective, down).
        """
        return self.y


    def to_board(self) -> str:
        """
        :returns: a string of length 2 encoding the square
                  in board-coordinates (from white's perspective, bottomleft).
                  examples: (5, 4) -> 'e4', (1, 1) -> 'a1'
        """
        return f"{chr(self.get_file() + (ord('a') - 1))}{self.get_rank()}"


    def from_board(self, coords: str) -> None:
        """
        :returns: a ChessSquare-Object resolved from a string of length
                  2 to a pair of integers corresponding to the file
                  and rank of a square on the board (from white's perspective, bottomleft).
                  examples: (5, 4) -> 'e4', (1, 1) -> 'a1'
        """
        if (len(coords) != 2):
            raise ValueError(f"invalid length for board-coordinates: '{coords}'")
        if (not coords[0].isalpha() or not coords[1].isnumeric()):
            raise ValueError(f"invalid board-coordinates: '{coords}'")
        self.x = ord(coords[0].lower()) - (ord('a') - 1) # 'a' -> 97
        self.y = int(coords[1])
        