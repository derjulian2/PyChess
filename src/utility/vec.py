
from typing import Generic, TypeVar, Iterable, Optional, TypeAlias, Self, Callable, Any
from copy import copy, deepcopy
import operator

Scalar: TypeAlias = Any

T = TypeVar("T")

class vec(Generic[T]):
    """
    type-generic vector-class.

    basically just a glorified list, as in that it 
    is guaranteed to have self.length elements and componentwise operations.
    """


    def __init__(self, 
                 *args,
                 default_value: Optional[T] = None,
                 max_len: Optional[int] = None) -> None:
        """
        initialization from iterable or multiple arguments of T:
            vec[T](1, 2, 3)   -> [1, 2, 3]
            vec[T]([1, 2, 3]) -> [1, 2, 3]
            vec[T]((1, 2, 3)) -> [1, 2, 3]
        """
        self.data: list[T]              = list()
        self.length: int                = 0
        self.default_value: Optional[T] = default_value
        # from a single iterable
        if (len(args) == 1 and isinstance(args[0], Iterable)):
            self.from_iterable(args[0], max_len=max_len)
        # from repr()-string
        elif (len(args) == 3
              and isinstance(args[0], str)
              and isinstance(args[1], str)
              and isinstance(args[2], str)):
            self.data          = eval(args[0])
            self.length        = eval(args[1])
            self.default_value = eval(args[2])
        # from multiple arguments
        elif (len(args) > 0):
            self.from_iterable(args, max_len=max_len)


    def __move__(self, other: Self) -> None:
        """
        'steals' the data from another instance.
        """
        self.data   = other.data
        self.length = other.length


    def __componentwise_op_unary__(self, op: Callable[[T], T]) -> Self:
        tmp: Self = deepcopy(self) # deepcopy to avoid problems with inheritance
        for i in range(len(self)):
            tmp[i] = op(self[i])
        return tmp

    
    def __componentwise_op_binary__(self, other: Iterable, op: Callable[[T, T], T]) -> Self:
        """
        creates a new vector-instance and initializes
        every element to op(a[i], b[i]).
        """
        if (len(self) != len(other)):
            raise ValueError("cannot operate on vectors of different sizes")
        tmp: Self = deepcopy(self) # deepcopy to avoid problems with inheritance
        for i in range(len(self)):
            tmp[i] = op(self[i], other[i])
        return tmp


    def __add__(self, other: Iterable | Scalar) -> Self:
        if (isinstance(other, Iterable)):
            return self.__componentwise_op_binary__(other, operator.add)
        return self.__componentwise_op_unary__(lambda x: operator.add(x, other))
    

    def __radd__(self, other: Iterable | Scalar) -> Self:
        return self.__add__(other)


    def __sub__(self, other: Iterable | Scalar) -> Self:
        if (isinstance(other, Iterable)):
            return self.__componentwise_op_binary__(other, operator.sub)
        return self.__componentwise_op_unary__(lambda x: operator.sub(x, other))


    def __mul__(self, other: Iterable | Scalar) -> Self:
        if (isinstance(other, Iterable)):
            return self.__componentwise_op_binary__(other, operator.mul)
        return self.__componentwise_op_unary__(lambda x: operator.mul(x, other))


    def __rmul__(self, other: Iterable | Scalar) -> Self:
        return self.__mul__(other)


    def __abs__(self) -> Self:
        return self.__componentwise_op_unary__(abs)


    def __eq__(self, other: Iterable | Scalar) -> bool:
        if (isinstance(other, Iterable)):
            return False not in self.__componentwise_op_binary__(other, operator.eq)
        return False not in self.__componentwise_op_unary__(lambda x: operator.eq(x, other))


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
        return f"vec('{self.data}','{self.length}','{self.default_value}')"


    def __str__(self) -> str:
        return str(self.data)
    
    
    def __hash__(self) -> int:
        """
        tuples the data contained in self.data and hashes that.
        """
        return hash((tuple(self.data), self.default_value))
    

    def clear(self) -> None:
        """
        clears the vector to exactly 'len(self)'
        elements of value zero.
        """
        self.data.clear()
        for _ in range(len(self)):
            self.data.append(copy(self.default_value))


    def resize(self, length: int) -> None:
        """
        resizes a vector to a given size.
        if the size is greater than the current, fill with zeroes.
        if it is smaller, elements will be cut.
        """
        diff = abs(len(self) - length)
        if (length > len(self)):
            for _ in range(diff):
                self.data.append(copy(self.default_value))
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
    """
    specialization for 2-element-vectors.
    """


    def __init__(self, *args, default_value: Optional[T] = None) -> None:
        super().__init__(*args, default_value=default_value, max_len=2)


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



class vec2i(vec2[int]):
    """
    specialization for 2-element integer-vectors.
    """


    def __init__(self, *args):
        super().__init__(*args, default_value=0)



class vec2f(vec2[float]):
    """
    specialization for 2-element float-vectors.
    """


    def __init__(self, *args):
        super().__init__(*args, default_value=0.0)