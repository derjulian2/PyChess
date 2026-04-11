
from gamelogic.piece  import ChessColor, ChessColor, ChessPieceType
from gamelogic.square import ChessSquare
from gamelogic.board  import ChessBoard, ChessBoardNavigator
from gamelogic.move   import ChessMove, InvalidMoveError, ChessMoveCastle, ChessMovePromotion

from typing import Optional
from copy import copy

class ChessGameProgress:

    def __init__(self) -> None:
        pass

    
    def in_progress(self) -> bool:
        pass

class ChessGameCastlingRights:

    def __init__(self) -> None:
        pass

class ChessGame:


    def __init__(self) -> None:
        self.state: ChessGameProgress      = ChessGameProgress()
        self.board: ChessBoard             = ChessBoard()
        self.rule50                        = 0
        
        self.player_to_move: ChessColor         = ChessColor.white
        self.en_passant: Optional[ChessSquare]        = None
        self.castling_rights: ChessGameCastlingRights = ChessGameCastlingRights()
        self.in_check: bool                           = False
        

    def __switch_player__(self) -> None:
        self.player_to_move = not self.player_to_move


    def __is_square_attacked__(self, sq: ChessSquare) -> None:
        for square, piece in self.board.get_pieces(color=not self.player_to_move):
            navigator = ChessBoardNavigator(self.board, square)
            if (sq in navigator.get_attackable_squares()):
                return True
        return False


    def __resolve_check_state__(self) -> None:
        king_square = self.board.get_king_square(self.player_to_move)
        if (king_square and self.__is_square_attacked__(king_square[0])):
            self.in_check = True
        else:
            self.in_check = False


    def __resolve_en_passant__(self) -> None:
        move = self.__last_move__()
        piece = self.board.get_piece(move.get_source_square())
        if ((piece.get_type() == ChessPieceType.pawn) and
            (abs(move.get_source_square() - move.get_target_square()) == (0, 2))):
            adjacent_squares = [ move.get_target_square() + (1, 0), move.get_target_square() + (-1, 0) ]
            for sq in adjacent_squares:
                if (not self.board.__out_of_bounds__(sq)):
                    other_piece = self.board.get_piece(sq)
                    if (other_piece.get_type() == ChessPieceType.pawn
                        and other_piece.get_color() != piece.get_color()):
                        self.en_passant = move.get_target_square()
        else:
            self.en_passant = None


    def __resolves_check__(self, move: ChessMove) -> bool:
        """
        applies the passed move to a copy of the current board
        and
        """
        return not self.__would_be_in_check__(move)


    def __would_be_in_check__(self, move: ChessMove) -> bool:
        """
        applies the passed move to a copy of the current board
        and returns if the king would be in check in that position.
        """
        board_cpy = copy(self.board)
        board_cpy.apply_move(move)
        king_square = board_cpy.get_king_square(self.player_to_move)
        if (king_square and self.__is_square_attacked__(king_square[0])):
            return True
        return False


    def __resolve_castling_rights__(self) -> None:
        if (isinstance(self.__last_move__(), ChessMoveCastle)):
            pass

    
    def __last_move__(self) -> ChessMove:
        return self.move_history[-1]


    def __update_game__(self) -> None:
        self.__resolve_check_state__()
        self.__resolve_en_passant__()
        self.__resolve_castling_rights__()
        self.__switch_player__()


    def __validate_move__(self, move: ChessMove) -> bool:
        navigator = ChessBoardNavigator(self.board, move.get_source_square())
        # regular move-handling: if square is reachable
        if (self.in_check):
            pass # somehow handle if move resolves check or not
        # also account for if the move would get king into check
        if (move.get_target_square() in navigator.get_all_squares()):
            return True
        # extra-rules: castling, en-passant, etc.
        if (isinstance(move, ChessMoveCastle)):
            pass
        elif (isinstance(move, ChessMovePromotion)):
            pass
        return False
    

    def make_move(self, move: ChessMove) -> None:
        if (not self.state.in_progress()):
            raise InvalidMoveError("game is finished. no further moves are possible.")
        if (not self.__validate_move__(move)):
            raise InvalidMoveError(f"move '{move}' cannot be made in the current position")
        self.__update_game__()
        self.board.apply_move(move)