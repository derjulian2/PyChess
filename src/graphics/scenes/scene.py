
from graphics.game_objects.game_object import *

from pygame_gui.core import UIElement
from pygame_gui import UIManager


class Scene:
    """
    a scene models a collection of GameObjects
    and UI-Elements.
    """

    def __init__(self, ui_manager: UIManager) -> None:
        self.game_objects: list[GameObject] = [ ]
        self.ui_elements: list[UIElement]   = [ ]
        self.ui_manager = ui_manager


    def attach_game_object(self, game_object: GameObject) -> None:
        """
        attaches a new object to this scene's list of game-objects.
        for the layered drawing, this list will be kept sorted after GameObject.layer.
        """
        for i in range(len(self.game_objects)):
            if self.game_objects[i].layer == game_object.layer:
                break
        self.game_objects.insert(i, game_object)


    def attach_ui_element(self, ui_element: UIElement) -> None:
        self.ui_elements.append(ui_element)


    def process_events(self, event: Event) -> None:
        """
        forwards .process_event()-call to all of it's game-objects and ui-elements.
        """
        for obj in self.game_objects:
            obj.process_events(event)
        self.ui_manager.process_events(event)


    def update(self, time_delta: float) -> None:
        """
        forwards .update()-call to all of it's game-objects and ui-elements.
        """
        for obj in self.game_objects:
            obj.update(time_delta)
        self.ui_manager.update(time_delta)


    def draw(self, target: Surface) -> None:
        """
        forwards .draw()-call to all of it's game-objects and ui-elements.
        performs layered rendering based on GameObject.layer. elements
        with lower layer will be drawn first.
        """
        for obj in self.game_objects:
            obj.draw(target)
        self.ui_manager.draw_ui(target)