
class ChessPiece(Entity):

    def __init__(self) -> None:
        self.add_component(DraggableComponent)