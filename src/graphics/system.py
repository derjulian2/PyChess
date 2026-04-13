
from graphics.entities.entity import Entity
from graphics.component import Component

from pygame import Event, Surface

class System:

    def __init__(self,
                 required_components: list[Component]) -> None:
        self.required_components: list[Component] = required_components


    def __has_components__(self, entity: Entity) -> bool:
        for comp in self.required_components:
            if (not entity.has_component(comp)):
                return False
        return True
    

    def __filter_entities__(self, entities: list[Entity]) -> list[Entity]:
        return list(filter(lambda e: self.__has_components__(e), entities))
    

    def execute(self, entities: list[Entity], *args):
        pass
        


from graphics.component import DrawableComponent

class EventSystem(System):

    def __init__(self) -> None:
        pass


    def execute(self, entites: list[Entity], event: Event):
        pass


class UpdateSystem(System):

    def execute(self, entities: list[Entity], time_delta: float) -> None:
        pass


class DrawSystem(System):


    def __init__(self, target: Surface) -> None:
        self.target: Surface = target


    def execute(self, entities: list[Entity]) -> None:
        for entity in self.__filter_entities__(entities):
            drawable_comp = entity.get_component(DrawableComponent)
            


