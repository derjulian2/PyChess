
from typing import Generic, TypeVar, Iterable, Optional, TypeAlias, Self, Callable

import operator

T = TypeVar("T")

class vec(Generic[T]):
    """
    type-generic vector-class.

    basically just a glorified list, as in that it 
    is guaranteed to have .length elements and componentwise operations.
    """

    def __init__(self, 
                 length: int, 
                 iterable: Optional[Iterable] = None) -> None:
        self.data: list[T] = list()
        self.length: int   = length
        self.clear()
        if (iterable):
            self.__from_iterable__(iterable)


    def __from_iterable__(self, iterable: Iterable) -> None:
        i = 0
        for elem in iterable:
            if (i >= len(self)):
                break
            self[i] = elem
            i += 1

    
    def __componentwise_op__(self, other: Self, op: Callable[[T, T], T]) -> Self:
        min_len = min(len(self), len(other))
        tmp: vec[T] = vec[T](min_len)
        tmp.resize(min_len)
        for i in range(min_len):
            tmp[i] = op(self[i], other[i])
        return tmp
    

    def __add__(self, other: Self) -> Self:
        return self.__componentwise_op__(other, operator.add)
    

    def __sub__(self, other: Self) -> Self:
        return self.__componentwise_op__(other, operator.sub)
    

    def __mul__(self, other: Self) -> Self:
        return self.__componentwise_op__(other, operator.mul)
    

    def __eq__(self, other: Self) -> bool:
        return False not in self.__componentwise_op__(other, operator.eq)


    def __len__(self) -> int:
        return self.length
    

    def __getitem__(self, i: int) -> T:
        return self.data[i]


    def __setitem__(self, i: int, v: T) -> None:
        self.data[i] = v


    def __repr__(self) -> str:
        return f"vec(length={self.length}, data={self.data})"


    def __str__(self) -> str:
        return str(self.data)
    

    def clear(self) -> None:
        """
        clears the vector to exactly 'len(self)'
        elements of value zero.
        """
        self.data.clear()
        for _ in range(len(self)):
            self.data.append(0)


    def resize(self, length: int) -> None:
        """
        resizes a vector to a given size.
        if the size is greater than the current, fill with zeroes.
        if it is smaller, elements will be cut.
        """
        diff = abs(len(self) - length)
        if (length > len(self)):
            for _ in range(diff):
                self.data.append(0)
        elif (length < len(self)):
            for _ in range(diff):
                self.data.pop()
        self.length = length



class vec2(vec[T]):


    def __init__(self, 
                 iterable: Optional[Iterable] = None) -> None:
        super().__init__(2, iterable)


    @property
    def x(self) -> T:
        return self[0]
    

    @x.setter
    def x(self, v: T) -> None:
        self[0] = v


    @property
    def y(self) -> T:
        return self[1]
    

    @y.setter
    def y(self, v: T) -> None:
        self[1] = v


vec2i: TypeAlias = vec2[int]
vec2f: TypeAlias = vec2[float]