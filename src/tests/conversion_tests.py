
from gamelogic.piece import *

print(ChessSquare(1, 1) == ChessSquare(1, 1))
print(ChessSquare(1, 1).to_board())
print(ChessSquare.from_board("e4") == ChessSquare(5, 4))