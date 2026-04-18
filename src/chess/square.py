
from utility.vec import vec2i

from typing import Self, Optional, Iterable


class ChessSquare(vec2i):
    """
    object that represents a valid chess-square
    on the board. 
    
    convertible from file-major integer-pair 
    to chess-notation and vice-versa (e.g. (5, 4) -> 'e4').
    """

    def __init__(self, *args):
        """
        inherits from utility.vec.vec2i, so any of the following
        construction-patterns is valid:
            ChessSquare(1, 1)              -> a1
            ChessSquare((1, 1))            -> a1
            ChessSquare(ChessSquare(1, 1)) -> a1

        additionally, from board-string is also valid:
            ChessSquare('a1')              -> a1
        """
        if (len(args) == 1 and isinstance(args[0], str)):
            super().__init__(0, 0)
            self.from_board(args[0])
        else:
            super().__init__(*args)
        

    
    def __str__(self) -> str:
        """
        :returns: a 2-character string that represents
                  the square in board-coordinates.
        """
        return self.to_board()
    

    def __repr__(self) -> str:
        """
        repr-overload. conversion from board-coordinates
        is used as it is more readable.
        :returns: same as str(self).
        """
        return f"ChessSquare('{self.to_board()}')"


    def get_file(self) -> int:
        """
        :returns: an integer indicating the 
                  file of the square (from white's perspective, starting left).
        """
        return self.x


    def get_rank(self) -> int:
        """
        :returns: an integer indicating the 
                  rank of the square (from white's perspective, starting at the bottom).
        """
        return self.y


    def to_board(self) -> str:
        """
        :returns: a string of length 2 encoding the square
                  in board-coordinates (from white's perspective, starting in the bottomleft).
                  examples: (5, 4) -> 'e4', (1, 1) -> 'a1'
        """
        return f"{chr(self.get_file() + (ord('a') - 1))}{self.get_rank()}"


    def from_board(self, s: str) -> None:
        """
        resolves a file-rank pair from a string encoding the coordinates.
        examples: (5, 4) -> 'e4', (1, 1) -> 'a1'

        :param s: the string encoding the board-coordinates.
        :raises ValueError: if s is not of length 2 or if s is not a letter-digit-pair.
        """
        if (len(s) != 2):
            raise ValueError(f"invalid length for board-coordinates: '{s}'")
        if (not s[0].isalpha() or not s[1].isnumeric()):
            raise ValueError(f"invalid board-coordinates: '{s}'")
        
        self.x = ord(s[0].lower()) - (ord('a') - 1) # 'a' -> 97
        self.y = int(s[1])
        