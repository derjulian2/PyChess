
from chess.common import ChessSquare
from chess.move import ChessMove, ChessMoveCastle, ChessMoveEnPassant, ChessMovePromotion, ChessCastleSquares
from chess.bitboard import ChessBitBoardPiece, ChessBitBoardSquare
from chess.game import ChessGame

from graphics.game_object import GameObject
from graphics.draggable import Draggable
from graphics.sprite import Sprite
from graphics.asset_manager import AssetManager

from utility.vec import vec2i
from utility.find import find, where

from pygame import Rect, Surface, Event, Color, draw

from typing import Self, Optional



class ChessPiece(Draggable, Sprite):
    """
    object for a draggable chess-piece.
    """

    def __init__(self,
                 square: ChessBitBoardSquare,
                 pos: vec2i,
                 size: int,
                 image: Surface,
                 callback) -> None:
        Draggable.__init__(self, Rect(pos, (size, size)), on_drag_end=lambda pos: callback(pos, self))
        Sprite.__init__(self, image, Rect(pos, (size, size)))

        self.bitboard_sq: ChessBitBoardSquare = square



class ChessBoard(GameObject):
    """
    game-object that represents
    a chess-board with all it's pieces.
    """
    
    light_square_color: Color     = Color.from_hex("#edd6b0")
    dark_square_color: Color      = Color.from_hex("#b88762")

    last_move_mask_color: Color = Color.from_hex("#f6eb72")


    def __init__(self,
                 pos: vec2i,
                 size: int,
                 asset_manager: AssetManager) -> None:
        super().__init__(Rect(pos, (size, size)))
        self.asset_manager: AssetManager    = asset_manager

        self.game: ChessGame                = ChessGame()
        self.last_move: Optional[ChessMove] = None
        self.__last_move_surf__: Surface    = Surface((self.__get_square_sidelen__(), self.__get_square_sidelen__()))
        self.__last_move_surf__.fill(self.last_move_mask_color)
        self.__last_move_surf__.set_alpha(200)

        self.flipped: bool            = False
        self.active_pieces: list[ChessPiece] = list()
        self.taken_pieces: list[ChessPiece]  = list()
        self.__set_position__()


    def process_events(self, event: Event) -> None:
        """
        forward process_events() to all pieces.
        """
        for piece in self.active_pieces:
            piece.process_events(event)


    def update(self, time_delta: float) -> None:
        """
        forward update() to all pieces.
        """
        for piece in self.active_pieces:
            piece.update(time_delta)


    def draw(self, target: Surface) -> None:
        """
        draws the entire chess-board with all it's pieces.
        """
        self.__draw_board__(target)
        self.__draw_pieces__(target)


    def __draw_board__(self, target: Surface) -> None:
        """
        draws the underlying chess-board-squares into
        the game-object's bounding-box.
        """
        for row in range(8):
            for column in range(8):
                sq    = ChessSquare(column + 1, row + 1)
                rect  = self.__get_square_rect__(sq)
                # checkerboard-formula:
                # credits: gknicker's answer at 
                # https://stackoverflow.com/questions/28788427/printing-a-checker-board-with-nested-loops-java
                if not ((column % 2 == 1) ^ (row % 2 == 0)):
                    color = ChessBoard.light_square_color
                else:
                    color = ChessBoard.dark_square_color
                
                draw.rect(target, color, rect)
                if (self.last_move):
                    if (sq == self.last_move.source or 
                        sq == self.last_move.target):
                        target.blit(self.__last_move_surf__, rect)


    def __draw_pieces__(self, target: Surface) -> None:
        """
        draws the individual piece-game-objects.
        """
        for piece in self.active_pieces:
            piece.draw(target)


    def __gen_new_piece__(self, square: ChessBitBoardSquare) -> ChessPiece:
        tmp = ChessPiece(square,
                         self.__get_square_rect__(square[0]).topleft,
                         self.__get_square_sidelen__(),
                         self.asset_manager.images[square[1]],
                         callback=lambda x, y: self.__callback_move__(x, y))
        return tmp


    def __set_position__(self) -> None:
        """
        resets the shown position from the position
        contained in the attached logical chess-board.
        this recreates new ChessPiece game-objects.
        """
        self.taken_pieces.extend(self.active_pieces)
        self.active_pieces.clear()
        for square in self.game.board.get_pieces():
            piece = where(lambda x: x.bitboard_sq[1] == square[1], self.taken_pieces)
            if (piece):
                self.taken_pieces.remove(piece)
                piece.bounding_box.topleft = self.__get_square_rect__(square[0]).topleft
                piece.bitboard_sq = square
            else:
                piece = self.__gen_new_piece__(square)
            self.active_pieces.append(piece)


    def __get_square_sidelen__(self) -> int:
        """
        returns the sidelength of a single square on screen.
        """
        return int(self.bounding_box.width / 8)


    def __get_square_rect__(self, square: ChessSquare) -> Rect:
        """
        returns the absolute rect of a chess-board-square
        identified by a row and column.
        """
        board_topleft  = self.bounding_box.topleft
        # offset by one to get zero for first row/column
        # flipped-logic required. needs helper-method.
        file = (square.file - 1)
        rank = (8 - square.rank)
        square_topleft = (board_topleft[0] + file * self.__get_square_sidelen__(),
                          board_topleft[1] + rank * self.__get_square_sidelen__()) 
        return Rect(square_topleft, (self.__get_square_sidelen__(), self.__get_square_sidelen__()))


    def __get_square_from_screen_pos__(self, pos: vec2i) -> ChessSquare:
        """
        returns a chess-square on the board from a screen-coordinate position.
        used in snapping pieces to the chess-grid.
        
        inverse to self.__get_square_rect__(...).
        """
        board_topleft = self.bounding_box.topleft
        tmp = ( int((pos[0] - board_topleft[0]) / self.__get_square_sidelen__()) + 1, 
               -int((pos[1] - board_topleft[1]) / self.__get_square_sidelen__()) + 8)
        return ChessSquare(tmp[0], tmp[1])


    def __callback_move__(self, pos: vec2i, piece: ChessPiece) -> None:
        try:
            square = self.__get_square_from_screen_pos__(pos)

            source = piece.bitboard_sq[0]
            target = square
            
            move           = ChessMove(source, target)
            possible_moves = self.game.gen_possible_moves()
            move_found = find(move, possible_moves)
            if (move_found):
                self.game.make_move(move_found)
            elif (len(possible_moves) == 0):
                raise ValueError("checkmate!")
            else:
                self.game.make_move(move)
            self.last_move = move

        except Exception as e:
            print(e)
            piece.bounding_box.topleft = self.__get_square_rect__(source).topleft
        self.__set_position__()


    def rebuild(self) -> None:
        """
        rebuild-override. resets the chess-position.
        """
        self.__set_position__()

    