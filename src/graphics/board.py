
from chess.common import ChessSquare
from chess.move import ChessMove
from chess.bitboard import ChessBitBoardPiece
from chess.game import ChessGame

from graphics.game_object import GameObject
from graphics.draggable import Draggable
from graphics.sprite import Sprite
from graphics.asset_manager import AssetManager

from utility.vec import vec2f

from pygame import Rect, Surface, Event, Color, draw

from typing import Self, Optional



class ChessPiece(Draggable, Sprite):
    """
    object for a draggable chess-piece.
    """

    def __init__(self,
                 pos: vec2f,
                 size: float,
                 image: Surface) -> None:
        Draggable.__init__(self, Rect(pos, (size, size)))
        Sprite.__init__(self, image, Rect(pos, (size, size)))



class ChessBoard(GameObject):
    """
    game-object that represents
    a chess-board with all it's pieces.
    """
    
    light_square_color: Color     = Color.from_hex("#eeeed2")
    dark_square_color: Color      = Color.from_hex("#769656")

    last_move_source_color: Color = Color.from_hex("#8e9a35")
    last_move_target_color: Color = Color.from_hex("#baca44")


    def __init__(self,
                 pos: vec2f,
                 size: float,
                 asset_manager: AssetManager) -> None:
        super().__init__(Rect(pos, (size, size)))
        self.asset_manager: AssetManager    = asset_manager

        self.game: ChessGame                = ChessGame()
        self.last_move: Optional[ChessMove] = None

        self.flipped: bool            = False
        self.pieces: list[ChessPiece] = list()
        self.__set_position_from_board__()


    def process_events(self, event: Event) -> None:
        """
        forward process_events() to all pieces.
        """
        for piece in self.pieces:
            piece.process_events(event)


    def update(self, time_delta: float) -> None:
        """
        forward update() to all pieces.
        """
        for piece in self.pieces:
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
                if ((column % 2 == 1) ^ (row % 2 == 0)):
                    color = ChessBoard.light_square_color
                else:
                    color = ChessBoard.dark_square_color
                
                if (self.last_move):
                    if (sq == self.last_move.source):
                        color = ChessBoard.last_move_source_color
                    elif (sq == self.last_move.target):
                        color = ChessBoard.last_move_target_color
                draw.rect(target, color, rect)


    def __draw_pieces__(self, target: Surface) -> None:
        """
        draws the individual piece-game-objects.
        """
        for piece in self.pieces:
            piece.draw(target)


    def __set_position_from_board__(self) -> None:
        """
        resets the shown position from the position
        contained in the attached logical chess-board.
        this recreates new ChessPiece game-objects.
        """
        self.pieces.clear()
        for square, piece in self.game.board.get_pieces():
            tmp = ChessPiece(self.__get_square_rect__(square).topleft,
                             self.__get_square_sidelen__(),
                             self.asset_manager.images[piece])
            self.pieces.append(tmp)


    def __get_square_sidelen__(self) -> float:
        """
        returns the sidelength of a single square on screen.
        """
        return float(self.bounding_box.width) / 8.0


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


    def __get_square_from_screen_pos__(self, pos: vec2f) -> ChessSquare:
        """
        returns a chess-square on the board from a screen-coordinate position.
        used in snapping pieces to the chess-grid.
        
        inverse to self.__get_square_rect__(...).
        """
        board_topleft = self.bounding_box.topleft
        tmp = ( int((pos[0] - board_topleft[0]) / self.__get_square_sidelen__()) + 1, 
               -int((pos[1] - board_topleft[1]) / self.__get_square_sidelen__()) + 8)
        return ChessSquare(tmp[0], tmp[1])


    # def __callback_snap_piece_to_grid__(self, pos: tuple[int, int], piece: ChessPiece) -> None:
    #     """
    #     callback to be passed to ChessPiece.on_drag_end. snaps the piece
    #     to the chess-grid from a screen-position.
    #     """
    #     try:
    #         square = self.__get_square_from_screen_pos__(pos)
    #         target = self.__get_square_rect__(square)
    #         piece.bounding_box.topleft = target.topleft
    #     except: # move out-of-bounds, set back to original pos
    #         source = self.__get_square_rect__(piece.logical_piece.square)
    #         piece.bounding_box.topleft = source.topleft


    def rebuild(self) -> None:
        """
        rebuild-override. resets the chess-position.
        """
        self.__set_position_from_board__()

    