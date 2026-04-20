
from pygame import image, Surface

from typing import Any
from os import PathLike


class AssetManager:
    """
    object that bundles asset-loading into one
    place, from which all game-objects can access them.
    """

    def __init__(self, 
                 images: dict[Any, PathLike]) -> None:
        self.image_paths                = images
        self.images: dict[Any, Surface] = dict()


    def load_images(self) -> None:
        """
        loads all images from their associated paths
        and keeps them accessible through an identifier-string.
        """
        for identifier in self.image_paths.keys():
            self.images[identifier] = image.load(self.image_paths[identifier])