
from typing import TypeVar, Type

ComponentType = TypeVar("ComponentType")


__entity_count__ = 0


def __get_new_id__() -> int:
    __id__ = __entity_count__
    __entity_count__ += 1
    return __id__


class Entity:


    def __init__(self) -> None:
        self.id: int    = __get_new_id__()
        self.components = [ ]


    def add_component(self, comp) -> None:
        self.components.append(comp)


    def has_component(self, comp) -> bool:
        return comp in self.components
    

    def get_component(self, comp: Type[ComponentType]) -> ComponentType:
        return self.components