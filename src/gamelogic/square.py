
class ChessSquare:
    """
    object that represents a valid chess-square
    on the board. is convertible from column-major
    integer-pair to chess-notation (e.g. (5, 4) -> 'e4').
    """

    def __init__(self, column: int, row: int):
        self.column = column
        self.row    = row
        
    
    def __eq__(self, other) -> bool:
        """
        equality-operator. row and column must match.
        """
        return self.column == other.column and self.row == other.row


    def to_board(self) -> str:
        """
        returns a 2-character-long string encoding
        a board-coordinate.
        the first row and first column corresponds to the a1 square.
        """
        return f"{chr(self.column + 96)}{self.row}"


    @classmethod
    def from_board(cls, coords: str):
        if (len(coords) != 2):
            raise ValueError("invalid board-coords")
        column = ord(coords[0].lower()) - 96 # 'a' -> 97
        row    = int(coords[1])
        return cls(row, column)