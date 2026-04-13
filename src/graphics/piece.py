
from graphics.entities.entity import Entity
from graphics.component import GameObjectComponent, DrawableComponent
from graphics.draggable import DraggableComponent


class ChessPiece(Entity):

    def __init__(self) -> None:
        self.add_component(GameObjectComponent)
        self.add_component(DrawableComponent)
        self.add_component(DraggableComponent)