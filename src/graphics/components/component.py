
from pygame import Rect, Color

class Component:

    def __init__(self) -> None:
        pass


class DrawableComponent:

    def __init__(self) -> None:
        self.layer: int


class GameObjectComponent:


    def __init__(self) -> None:
        self.bounding_box: Rect
        self.color: Color
