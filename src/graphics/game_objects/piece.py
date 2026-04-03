
import gamelogic.piece as logic

from graphics.game_objects.draggable import *
from asset_manager import AssetManager

class ChessPiece(Draggable, GameObject):
    """
    base-class for a moveable chess-piece.
    """

    def __init__(self,
                 asset_manager: AssetManager,
                 piece: logic.ChessPiece,
                 pos: tuple[int, int],
                 size: float) -> None:
        Draggable.__init__(self, asset_manager, Rect(pos, (size, size))),
        GameObject.__init__(self, asset_manager, self.bounding_box)
        self.logical_piece: logic.ChessPiece = piece
        self.image: Surface                  = None
        self.__fit_image__()


    def __fit_image__(self) -> None:
        img = self.asset_manager.images[(self.logical_piece.piece_color, self.logical_piece.piece_type)]
        self.image = pygame.transform.smoothscale(img, self.bounding_box.size)


    def draw(self, target: Surface) -> None:
        """
        draws the sprite to the target-surface.
        """
        target.blit(self.image, self.bounding_box)


    def rebuild(self) -> None:
        """
        rescales the image to the bounding-box.
        """
        self.__fit_image__()
        Draggable.rebuild(self)