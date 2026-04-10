
from typing import Callable, Optional
from graphics.game_objects.game_object import *

import pygame


class DraggableComponent(GameObject):
    """
    base-class for any draggable game-object.
    
    because python doesn't have the inheritance diamond-problem, we can
    easily inherit from multiple 'GameObject'-base-classes and still
    refer to the same set of fields.
    """
    
    def __init__(self, 
                 asset_manager: AssetManager,
                 bounding_box: Rect,
                 color: Color | None = None, 
                 layer: int = 0,
                 on_drag_start: Optional[Callable[[tuple[int, int]], None]] = None,
                 on_drag_end: Optional[Callable[[tuple[int, int]], None]] = None) -> None:
        super().__init__(asset_manager, bounding_box, color, layer)
        self.is_dragging: bool = False
        self.on_drag_start: Optional[Callable[[tuple[int, int]], None]] = on_drag_start
        self.on_drag_end: Optional[Callable[[tuple[int, int]], None]]   = on_drag_end


    def process_events(self, event: Event) -> None:
        """
        draggable-logic: record when mouse is pressed and released
        and update the is_dragging state accordingly.
        """
        if (event.type == pygame.MOUSEBUTTONDOWN):
            if (Rect(pygame.mouse.get_pos(), (1, 1)) in self.bounding_box):
                self.is_dragging = True
                pygame.mouse.get_rel() # call once to reset since-last-call
                if (self.on_drag_start):
                    self.on_drag_start(pygame.mouse.get_pos())
        elif (event.type == pygame.MOUSEBUTTONUP and self.is_dragging):
            self.is_dragging = False
            if (self.on_drag_end):
                self.on_drag_end(pygame.mouse.get_pos())


    def update(self, time_delta: float) -> None:
        """
        reposition the game-object's bounding-box if it is dragged.
        """
        if (self.is_dragging):
            self.bounding_box = self.bounding_box.move(pygame.mouse.get_rel())


    def rebuild(self) -> None:
        self.is_dragging = False