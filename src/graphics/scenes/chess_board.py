
from graphics.scenes.scene import Scene
from graphics.game_objects.board import ChessBoard

from pygame_gui import UIManager

class ChessBoardScene(Scene):
    """
    scene that draws the chess-board and
    the move-history UI to the player.
    """

    def __init__(self, ui_manager: UIManager) -> None:
        super().__init__(ui_manager)
        self.board: ChessBoard
        self.__setup_board__()


    def __setup_board__(self) -> None:
        self.board = ChessBoard()
        self.attach_game_object(self.board)


    def __setup_gui__(self) -> None:
        pass