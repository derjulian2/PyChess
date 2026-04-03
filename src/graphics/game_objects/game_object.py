
from pygame import *

class GameObject:
    """
    abstract-base-class for any game-object
    to be saved as part of a scene.
    """

    def __init__(self, 
                 bounding_box: Rect, 
                 color: Color, 
                 layer: int) -> None:
        self.bounding_box: Rect = bounding_box
        self.color: Color       = color
        self.layer: int         = layer # modifying this directly doesn't change the layer, maybe hold .scene member and .change_layer() func
    

    def process_events(self, event: Event) -> None:
        """
        base-method to override.
        """
        pass


    def update(self, time_delta: float) -> None:
        """
        base-method to override.
        """
        pass


    def draw(self, target: Surface) -> None:
        """
        base-method to override.
        """
        pass
