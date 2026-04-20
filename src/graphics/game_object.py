
from graphics.asset_manager import AssetManager

from pygame import Rect, Color, Event, Surface

from typing import Optional


class GameObject:
    """
    abstract-base-class for any game-object
    to be saved as part of a scene.

    maybe change this to a component-based system i.e. 
    every game-object has a list of components that it stores.
    """


    def __init__(self,
                 bounding_box: Rect, 
                 color: Optional[Color] = None) -> None:
        self.bounding_box: Rect     = bounding_box
        self.color: Optional[Color] = color
    

    def process_events(self, event: Event) -> None:
        """
        base-method to override. this method will be called
        during the window's event-loop and will pass every event in here once
        (so it could be called multiple times per frame if multiple events occured).
        """
        pass


    def update(self, time_delta: float) -> None:
        """
        base-method to override. this method will be called after
        every frame after the event-loop and before drawing.
        """
        pass


    def draw(self, target: Surface) -> None:
        """
        base-method to override. this method will be called
        at the end of each frame.
        """
        pass


    def rebuild(self) -> None:
        """
        base-method to override. this method will only be called
        explicitly to reload all of a GameObject's assets or perform
        some other costly operation that should not be performed every frame.
        """
        pass