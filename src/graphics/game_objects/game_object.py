
from pygame import *
from asset_manager import AssetManager

class GameObject:
    """
    abstract-base-class for any game-object
    to be saved as part of a scene.

    maybe change this to a component-based system i.e. 
    every game-object has a list of components that it stores.
    """

    def __init__(self,
                 asset_manager: AssetManager,
                 bounding_box: Rect, 
                 color: Color | None = None, 
                 layer: int = 0) -> None:
        self.asset_manager: AssetManager = asset_manager
        self.bounding_box: Rect          = bounding_box
        self.color: Color | None         = color
        self.layer: int                  = layer 
        # modifying .layer directly doesn't actually change the layer
        # maybe hold .scene member and .change_layer() func
    

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