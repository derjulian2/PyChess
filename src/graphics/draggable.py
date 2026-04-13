
from graphics.component import Component
from utility.vec import vec2i

from typing import Optional, Callable
from dataclasses import dataclass


@dataclass
class DraggableComponent(Component):

    is_dragging: bool                                = False
    on_drag_start: Optional[Callable[[vec2i], None]] = None
    on_drag_end: Optional[Callable[[vec2i], None]]   = None


from graphics.component import GameObjectComponent
from graphics.draggable import DraggableComponent
from graphics.system import System

import pygame
from pygame import Event, Rect


class DraggableSystem(System):
    

    def execute(self, entities, event: Event) -> None:
        for entity in entities:
            bounding_box_comp: GameObjectComponent = None
            draggable_comp: DraggableComponent = None
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


    def update(self, entities, time_delta) -> None:
        """
        reposition the game-object's bounding-box if it is dragged.
        """
        if (self.is_dragging):
            self.bounding_box = self.bounding_box.move(pygame.mouse.get_rel())