
from gamelogic.piece import ChessPiece, ChessPlayerColor, ChessPieceColor, ChessPieceType
from gamelogic.board  import ChessBoard
from gamelogic.square import ChessSquare
from gamelogic.move   import ChessMove, ChessMoveCastle, ChessMovePromotion, InvalidMoveError, MoveRule

from typing import Optional
from enum import Enum

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


class ChessGameState(Enum):
    in_progress = 0
    in_check    = 1
    checkmate   = 2


class ChessGame:
    """
    state-like object that holds information about
    a full chess-match-instance.
    """

    def __init__(self) -> None:
        self.state: ChessGameState             = ChessGameState.in_progress
        self.player_to_move: ChessPlayerColor  = ChessPlayerColor.white
        self.board: ChessBoard                 = ChessBoard()
        self.en_passant: Optional[ChessSquare] = None 
        self.move_history: list[ChessMove]     = list()
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
        if (not self.is_move_legal(move)):
            raise InvalidMoveError(f"illegal move in the current position: '{move}'")
        piece = self.board.get_piece(move.source_square).get_piece()
        self.board.get_piece(move.source_square).piece = None
        match (move):
            case (ChessMovePromotion()):
                self.board.get_piece(move.target_square).piece = ChessPiece(move.promotion, piece.get_color())
            case (ChessMoveCastle()):
                pass
            case (ChessMove()):
                self.board.get_piece(move.target_square).piece = piece


    def __update_game__(self) -> None:
        """
        updates the internal game-state.
        """
        pass


    def __switch_player_to_move__(self) -> None:
        self.player_to_move = not self.player_to_move


    def __check_castle__(self, move: ChessMoveCastle) -> bool:
        return move.side in self.castling_rights[self.player_to_move]


    def __is_in_check__(self) -> bool:
        return self.is_square_attacked(
                    self.player_to_move, 
                    self.board.get_pieces(color=self.player_to_move, type=ChessPieceType.king))


    def is_move_legal(self, move: ChessMove) -> bool:
        """
        matches the passed move with the current board and decides
        if that move is legal to make.
        """
        if (isinstance(move, ChessMoveCastle)):
            return self.__check_castle__(move)

        # handle regular moves
        valid_squares = list()
        for sq in MoveRule.get_moves(move.get_source_square()):
            try:
                if (not self.board.get_piece(sq).has_piece()):
                    valid_squares.append(sq)
            except:
                continue

        for sq in MoveRule.get_attacks(move.get_source_square()):
            try:
                if (self.board.get_piece(sq).has_piece()):
                    valid_squares.append(sq)
            except:
                continue
        # extra-rules
        if (self.__is_in_check__()):
            pass

        if (move.get_source_square().get_piece() == ChessPieceType.pawn and self.en_passant):
            valid_squares.append(self.en_passant)

        return move.get_target_square() in valid_squares
            
    

    def make_move(self, move: ChessMove) -> None:
        """
        tests if the passed move is legal and if so applies 
        it to the board and switches the player to move.
        """
        self.__apply_move__(move)
        self.__switch_player_to_move__()
        self.move_history.append(move)


    def is_square_attacked(self, 
                           color: ChessPlayerColor,
                           sq: ChessSquare) -> bool:
        opponent_piece_squares = self.board.get_pieces(color= not color)
        for square in opponent_piece_squares:
            if sq in MoveRule.get_attacks(square):
                return True
        return False
