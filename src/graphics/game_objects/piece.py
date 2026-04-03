
from graphics.game_objects.game_object import *


class ChessPiece(GameObject):
    """
    base-class for a moveable chess-piece.
    """

    def __init__(self,
                 pos: tuple[int, int]) -> None:
        self.sprite


    def process_events(self, event: Event) -> None:
        pass


    def update(self, time_delta: float) -> None:
        pass


    def draw(self, target: Surface) -> None:
        pass


class ChessPiecePawn(ChessPiece):
    pass