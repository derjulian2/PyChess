
from graphics.game_object import GameObject

from pygame import Rect, Surface, transform


class Sprite(GameObject):
    """
    combines image and bounding-box
    into a renderable game-object.
    """


    def __init__(self, 
                 image: Surface,
                 bounding_box: Rect) -> None:
        super().__init__(bounding_box)
        self.image: Surface        = image
        self.scaled_image: Surface = None
        self.__fit_image__()


    def __fit_image__(self) -> None:
        """
        scales the passed source-image to the bounding-box.
        """
        self.scaled_image = transform.smoothscale(self.image, self.bounding_box.size)


    def draw(self, target: Surface) -> None:
        """
        draws the sprite to the target-surface.
        """
        target.blit(self.scaled_image, self.bounding_box)


    def rebuild(self) -> None:
        """
        rescales the image to the bounding-box.
        """
        self.__fit_image__()