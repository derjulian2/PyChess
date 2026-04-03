
from gamelogic.board import *


class ChessMove:
    """
    type that wraps a string and guarantees that
    this string holds a valid PGN-chess-move, or raises an error otherwise.
    """

    def __init__(self, mv: str) -> None:
        self.move = mv
        if (not self.is_PGN_correct()):
            raise ValueError("not a valid PGN-chess-move")


    def is_PGN_correct(self) -> bool:
        """
        returns False if self.move does not
        form a valid chess-move-expression according to
        Portable-Game-Notation (https://de.wikipedia.org/wiki/Portable_Game_Notation).
        """
        pass



class ChessCastlingRights:
    """
    object that holds information about a
    single player's castling-rights.

    this does not hold information about wether a player
    is currently allowed to castle (which might not be the case
    although the player has the according castling-rights).
    such information must be determined through a board's position.
    """
    def __init__(self, color: ChessPlayerColor) -> None:
        self.player_color    = color
        self.kingside: bool  = True
        self.queenside: bool = True


    def to_fen(self) -> str:
        res: str = str()
        if (self.kingside):
            res += "k"
        if (self.queenside):
            res += "q"
        if (self.player_color == ChessPlayerColor.white):
            res = res.upper()
        return res



class ChessGame:
    """
    state-like object that holds information about
    a full chess-match-instance.
    """

    def __init__(self) -> None:
        self.player_to_move: ChessPlayerColor = ChessPlayerColor.white
        self.board: ChessBoard                = ChessBoard()
        self.en_passant: bool                 = False
        self.move_history: list[ChessMove]    = list()
        self.castling_rights: list[ChessCastlingRights] = [ 
            ChessCastlingRights(color) for color in ChessPlayerColor
        ]

    """
    to and from Forsyth–Edwards Notation (FEN) (https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation)
    """

    def to_fen(self) -> str:
        return (self.board.to_fen() 
                + " " + self.__player_to_move_to_fen__()
                + " " + str().join([ c.to_fen() for c in self.castling_rights ])
                + " " + self.__en_passant_to_fen__()
                + " " + self.__half_moves_to_fen__()
                + " " + self.__move_count_to_fen__())


    @classmethod
    def from_fen(cls, fen: str):
        return cls()
    

    def __player_to_move_to_fen__(self) -> str:
        match self.player_to_move:
            case ChessPlayerColor.white:
                return "w"
            case ChessPlayerColor.black:
                return "b"


    def __get_last_en_passant__(self) -> str:
        pass


    def __en_passant_to_fen__(self) -> str:
        if (self.en_passant):
            return self.__get_last_en_passant__()
        return "-"
    

    def __half_moves_to_fen__(self) -> str:
        return str(0)


    def __move_count_to_fen__(self) -> str:
        return str(self.move_count() + 1)
    

    """
    to and from Portable-Game-Notation (PGN) (https://en.wikipedia.org/wiki/Portable_Game_Notation).
    """

    def to_pgn(self) -> str:
        return ""


    @classmethod
    def from_pgn(cls, pgn: str):
        return cls()


    def move_count(self) -> int:
        return int(len(self.move_history) / 2)

    """
    game-logic implementation. 
    
    this part of the code actually verifies if a chess-move is valid 
    for a given board-instance and then performs the move on the existing 
    board-data, while also updating any state variables (like en-passant or castling-rights).
    """

    def __apply_move__(self, move: ChessMove) -> None:
        pass


    def __switch_player_to_move__(self) -> None:
        match (self.player_to_move):
            case (ChessPlayerColor.white):
                self.player_to_move = ChessPlayerColor.black
            case (ChessPlayerColor.black):
                self.player_to_move = ChessPlayerColor.white


    def is_move_legal(self, move: ChessMove) -> bool:
        """
        matches the passed move with the current board and decides
        if that move is legal to make.
        """
        return False
    

    def make_move(self, move: ChessMove) -> bool:
        """
        tests if the passed move is legal and if so applies 
        it to the board and switches the player to move.
        """
        if (not self.is_move_legal(move)):
            return False
        self.__apply_move__(move)
        self.__switch_player_to_move__()
        self.move_history.append(move)