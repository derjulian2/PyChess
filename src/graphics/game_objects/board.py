
import gamelogic.board as logic

from pygame import Rect, Surface, Event, Color
from graphics.game_objects.game_object import GameObject
from graphics.game_objects.piece import ChessPiece
from asset_manager import AssetManager

import pygame.draw as pydraw

class ChessBoard(GameObject):
    """
    game-object that represents
    a chess-board with all it's pieces.
    """
    
    light_square_color: Color = Color.from_hex("#eeeed2")
    dark_square_color: Color  = Color.from_hex("#769656")

    def __init__(self,
                 asset_manager: AssetManager,
                 board: logic.ChessBoard,
                 pos: tuple[int, int],
                 size: float) -> None:
        super().__init__(asset_manager, Rect(pos, (size, size)))
        self.logical_board: logic.ChessBoard = board
        self.pieces: list[ChessPiece]        = list()
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
        for row in range(self.logical_board.board_rows):
            for column in range(self.logical_board.board_columns):
                rect  = self.__get_square_rect__(logic.ChessSquare(column + 1, row + 1))
                # checkerboard-formula:
                # credits: gknicker's answer at 
                # https://stackoverflow.com/questions/28788427/printing-a-checker-board-with-nested-loops-java
                if ((column % 2 == 1) ^ (row % 2 == 0)):
                    color = ChessBoard.light_square_color
                else:
                    color = ChessBoard.dark_square_color
                pydraw.rect(target, color, rect)


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
        for piece in self.logical_board.get_pieces():
            tmp = ChessPiece(self.asset_manager,
                             piece,
                             self.__get_square_rect__(piece.get_square()).topleft,
                             self.__get_square_sidelen__(),
                             on_drag_end=lambda pos, dragged_piece: self.__callback_snap_piece_to_grid__(pos, dragged_piece))
            self.pieces.append(tmp)


    def __get_square_sidelen__(self) -> int:
        """
        returns the sidelength of a single square on screen.
        """
        return int(self.bounding_box.width / self.logical_board.board_rows)


    def __get_square_rect__(self, square: logic.ChessSquare) -> Rect:
        """
        returns the absolute rect of a chess-board-square
        identified by a row and column.
        """
        board_topleft  = self.bounding_box.topleft
        # offset by one to get zero for first row/column
        cols = (square.get_column() - 1)
        rows = (self.logical_board.board_rows - square.get_row())
        square_topleft = (board_topleft[0] + cols * self.__get_square_sidelen__(),
                          board_topleft[1] + rows * self.__get_square_sidelen__()) 
        return Rect(square_topleft, (self.__get_square_sidelen__(), self.__get_square_sidelen__()))


    def __get_square_from_screen_pos__(self, pos: tuple[int, int]) -> logic.ChessSquare:
        """
        returns a chess-square on the board from a screen-coordinate position.
        used in snapping pieces to the chess-grid.
        
        inverse to self.__get_square_rect__(...).
        """
        board_topleft = self.bounding_box.topleft
        tmp = ( int((pos[0] - board_topleft[0]) / self.__get_square_sidelen__()) + 1, 
               -int((pos[1] - board_topleft[1]) / self.__get_square_sidelen__()) + self.logical_board.board_rows)
        if (tmp[0] <= 0 or tmp[1] <= 0 or
            tmp[0] > self.logical_board.board_columns or
            tmp[1] > self.logical_board.board_rows):
            raise ValueError("position not on a chess-square")
        return logic.ChessSquare(tmp[0], tmp[1])


    def __callback_snap_piece_to_grid__(self, pos: tuple[int, int], piece: ChessPiece) -> None:
        """
        callback to be passed to ChessPiece.on_drag_end. snaps the piece
        to the chess-grid from a screen-position.
        """
        try:
            square = self.__get_square_from_screen_pos__(pos)
            target = self.__get_square_rect__(square)
            piece.bounding_box.topleft = target.topleft
        except: # move out-of-bounds, set back to original pos
            source = self.__get_square_rect__(piece.logical_piece.square)
            piece.bounding_box.topleft = source.topleft


    def rebuild(self) -> None:
        """
        rebuild-override. resets the chess-position.
        """
        self.__set_position_from_board__()

    