
from typing import Generic, TypeVar, Iterable, Optional, TypeAlias, Self, Callable
from copy import copy, deepcopy
import operator


T = TypeVar("T")

class vec(Generic[T]):
    """
    type-generic vector-class.

    basically just a glorified list, as in that it 
    is guaranteed to have self.length elements and componentwise operations.
    """


    def __init__(self, 
                 *args, 
                 max_len: Optional[int] = None) -> None:
        """
        initialization from iterable or multiple arguments of T:
            vec[T](1, 2, 3)   -> [1, 2, 3]
            vec[T]([1, 2, 3]) -> [1, 2, 3]
            vec[T]((1, 2, 3)) -> [1, 2, 3]
        """
        self.data: list[T] = list()
        self.length: int   = 0
        if (len(args) == 1 and isinstance(args[0], Iterable)):
            self.from_iterable(args[0], max_len=max_len)
        elif (len(args) == 1 and isinstance(args[0], int)):
            self.resize(args[0])
        elif (len(args) > 0):
            self.from_iterable(args, max_len=max_len)


    def __move__(self, other: Self) -> None:
        """
        'steals' the data from another instance.
        """
        self.data   = other.data
        self.length = other.length


    def __componentwise_op_unary__(self, op: Callable[[T], T]) -> Self:
        tmp: Self = deepcopy(self)
        for i in range(len(self)):
            tmp[i] = op(self[i])
        return tmp

    
    def __componentwise_op_binary__(self, other: Iterable, op: Callable[[T, T], T]) -> Self:
        """
        creates a new vector-instance and initializes
        every element to op(a[i], b[i]).
        """
        min_len = min(len(self), len(other))
        tmp: Self = deepcopy(self)
        tmp.resize(min_len)
        for i in range(min_len):
            tmp[i] = op(self[i], other[i])
        return tmp


    def __add__(self, other: Iterable) -> Self:
        return self.__componentwise_op_binary__(other, operator.add)
    

    def __sub__(self, other: Iterable) -> Self:
        return self.__componentwise_op_binary__(other, operator.sub)
    

    def __mul__(self, other: Iterable) -> Self:
        return self.__componentwise_op_binary__(other, operator.mul)
    

    def __abs__(self) -> Self:
        return self.__componentwise_op_unary__(abs)


    def __eq__(self, other: Iterable) -> bool:
        return False not in self.__componentwise_op_binary__(other, operator.eq)


    def __iter__(self) -> T:
        for elem in self.data:
            yield elem


    def __len__(self) -> int:
        """
        :returns: the current fixed-length of the vector.
        """
        return self.length
    

    def __getitem__(self, i: int) -> T:
        return self.data[i]


    def __setitem__(self, i: int, v: T) -> None:
        self.data[i] = v


    def __repr__(self) -> str:
        return f"vec(length={self.length}, data={self.data})"


    def __str__(self) -> str:
        return str(self.data)
    
    
    def __hash__(self) -> int:
        """
        tuples the data contained in self.data and hashes that.
        """
        return tuple(self.data).__hash__()
    

    def clear(self) -> None:
        """
        clears the vector to exactly 'len(self)'
        elements of value zero.
        """
        self.data.clear()
        for _ in range(len(self)):
            self.data.append(None)


    def resize(self, length: int) -> None:
        """
        resizes a vector to a given size.
        if the size is greater than the current, fill with zeroes.
        if it is smaller, elements will be cut.
        """
        diff = abs(len(self) - length)
        if (length > len(self)):
            for _ in range(diff):
                self.data.append(None)
        elif (length < len(self)):
            for _ in range(diff):
                self.data.pop()
        self.length = length


    def from_iterable(self, 
                      iterable: Iterable, 
                      *, 
                      max_len: Optional[int] = None) -> Self:
        """
        initializes from an iterable.

        :param iterable: the range to generate from.
        :param max_len:  limits the vector-length even if the iterable is longer.
        """
        if (max_len):
            self.resize(max_len)
        else:
            self.resize(len(iterable))
        i = 0
        for elem in iterable:
            if (i >= self.length):
                break
            self[i] = elem
            i += 1
    


class vec2(vec[T]):


    def __init__(self, *args) -> None:
        super().__init__(*args, max_len=2)


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