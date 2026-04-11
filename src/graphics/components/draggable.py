
from graphics.components.component import Component
from utility.vec import vec2i

from typing import Optional, Callable


class DraggableComponent(Component):


    def __init__(self,
                 on_drag_start: Optional[Callable[[vec2i], None]] = None,
                 on_drag_end: Optional[Callable[[vec2i], None]] = None) -> None:
        self.is_dragging: bool = False
        self.on_drag_start: Optional[Callable[[vec2i], None]] = on_drag_start
        self.on_drag_end: Optional[Callable[[vec2i], None]]   = on_drag_end