

from typing import TypeVar, Generic, Iterable, Optional, Self, Dict, Set, Generator, List, TypeAlias, Any


T = TypeVar('T')


class queue(list[T]):

    def enqueue(self, object: Any) -> None:
        self.append(object)

    def dequeue(self) -> Any:
        return self.pop(0)
    
    def is_empty(self) -> bool:
        return len(self) == 0



class tree_node(Generic[T]):

    def __init__(self,
                 parent: Self,
                 value: Optional[T] = None,
                 children: Optional[Iterable[T]] = None) -> None:
        self.value: Optional[T]           = value
        self.parent: tree_node            = parent
        self.children: list[tree_node[T]] = list()

    
    def is_leaf(self) -> bool:
        return len(self.children) == 0


    def is_root(self) -> bool:
        return self.parent is None
    

    def depth(self) -> int:
        res  = 0
        iter = self
        while not (iter.is_root()):
            res += 1
            iter = iter.parent
        return res



class tree(Generic[T]):


    def __init__(self,
                 *args) -> None:
        self.root: tree_node = tree_node(None) 

        if (len(args) == 1 and isinstance(args[0], Iterable)):
            self.from_nested(args[0])


    @staticmethod
    def __from_nested_impl__(__node__: tree_node,
                             __iterable__: Iterable) -> None:
        if (isinstance(__iterable__, Dict)):
            for node_value, node_children in __iterable__.items():
                __new_node__ = tree_node(__node__, node_value) 
                __node__.children.append(__new_node__)
                tree.__from_nested_impl__(__new_node__, node_children)
        elif (isinstance(__iterable__, Set)):
            for node_value in __iterable__:
                __new_node__ = tree_node(__node__, node_value) 
                __node__.children.append(__new_node__)
        else:
            raise TypeError("unsupported iterable-construction. try a nested dictionary and sets.")


    @staticmethod
    def __depth_first_impl__(__node__: tree_node) -> Generator[tree_node[T]]:
        yield __node__
        for __child__ in __node__.children:
            yield from tree.__depth_first_impl__(__child__)


    @staticmethod
    def __breadth_first_impl__(__node__: tree_node) -> Generator[tree_node[T]]:
        __queue__: queue[tree_node] = queue()
        __queue__.enqueue(__node__)
        while not (__queue__.is_empty()):
            __cur__: tree_node = __queue__.dequeue()
            yield __cur__
            for __child__ in __cur__.children:
                __queue__.enqueue(__child__)


    def from_nested(self, iterable: Iterable) -> None:
        tree.__from_nested_impl__(self.root, iterable)


    def depth_first(self) -> Generator[tree_node[T]]:
        yield from tree.__depth_first_impl__(self.root)


    def breadth_first(self) -> Generator[tree_node[T]]:
        yield from tree.__breadth_first_impl__(self.root)