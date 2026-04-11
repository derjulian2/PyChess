
from graphics.entities.entity import Entity
from graphics.systems.system import System, EventSystem, DrawSystem
from asset_manager import AssetManager

from pygame_gui.core import UIElement
from pygame_gui import UIManager


class Scene:
    """
    a scene models a collection of GameObjects
    and UI-Elements.
    """

    def __init__(self, ui_manager: UIManager, asset_manager: AssetManager) -> None:
        self.entites: list[Entity]        = list()
        self.systems: list[System]        = list()


    def execute(self) -> None:
        for sys in self.systems:
            sys.execute(self.entites)