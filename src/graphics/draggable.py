
from graphics.game_object import GameObject

from utility.vec import vec2i

from pygame import Rect, Event, mouse, MOUSEBUTTONDOWN, MOUSEBUTTONUP

from typing import Callable, Optional


class Draggable(GameObject):
    """
    base-class for any draggable game-object.
    
    because python doesn't have the inheritance diamond-problem, we can
    easily inherit from multiple 'GameObject'-base-classes and still
    refer to the same set of fields.
    """
    
    def __init__(self, 
                 bounding_box: Rect,
                 on_drag_start: Optional[Callable[[vec2i], None]] = None,
                 on_drag_end: Optional[Callable[[vec2i], None]] = None) -> None:
        GameObject.__init__(self, bounding_box)
        self.is_dragging: bool = False
        self.on_drag_start: Optional[Callable[[vec2i], None]] = on_drag_start
        self.on_drag_end: Optional[Callable[[vec2i], None]]   = on_drag_end


    def process_events(self, event: Event) -> None:
        """
        draggable-logic: record when mouse is pressed and released
        and update the is_dragging state accordingly.
        """
        if (event.type == MOUSEBUTTONDOWN):
            if (Rect(mouse.get_pos(), (1, 1)) in self.bounding_box):
                self.is_dragging = True
                mouse.get_rel() # call once to reset since-last-call
                if (self.on_drag_start):
                    self.on_drag_start(mouse.get_pos())
        elif (event.type == MOUSEBUTTONUP and self.is_dragging):
            self.is_dragging = False
            if (self.on_drag_end):
                self.on_drag_end(mouse.get_pos())


    def update(self, time_delta: float) -> None:
        """
        reposition the game-object's bounding-box if it is dragged.
        """
        if (self.is_dragging):
            self.bounding_box = self.bounding_box.move(mouse.get_rel())


    def rebuild(self) -> None:
        self.is_dragging = False