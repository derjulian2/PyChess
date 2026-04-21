

from graphics.ui_infodialog import UIInfoDialog


class UIPromotionDialog(UIInfoDialog):
    """
    dialog-window that prompts the user
    to choose the piece that they want to
    promote a pawn to.
    """


    def __init__(self) -> None:
        super().__init__()