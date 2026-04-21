
from pygame_gui.elements import UIWindow


class UIInfoDialog(UIWindow):
    """
    dialog-window used for displaying
    information to the player or receiving some
    relevant input to the game.
    """


    def __init__(self) -> None:
        super().__init__()