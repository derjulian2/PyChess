
from typing import TypeVar, Type

ComponentType = TypeVar("ComponentType")


class Entity:


    def __init__(self) -> None:
        self.components = [ ]


    def add_component(self, comp) -> None:
        self.components.append(comp)


    def has_component(self, comp) -> bool:
        return comp in self.components
    

    def get_component(self, comp: Type[ComponentType]) -> ComponentType:
        return self.components