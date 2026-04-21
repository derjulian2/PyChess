
from typing import Iterable, Callable, TypeVar, Optional
from operator import eq

T = TypeVar('T')


def where(pred: Callable[[T], bool],
          iterable: Iterable[T]) -> Optional[T]:
    """
    searches for the first object in a range
    for which the pred(obj) evaluates to true.

    :param pred: the condition to check for every element.
    :param iterable: the range to search in.

    :returns: the first object of the range for which
              pred(elem) evaluated to true, or None
              if no such object exists.
    """
    for elem in iterable:
        if (pred(elem)):
            return elem
    return None


def find(object: T,
         iterable: Iterable[T]) -> Optional[T]:
    """
    searches for the first object in a range by comparison 
    to another value of that type.

    :param object: the value to search for.
    :param iterable: the range to search in.

    :returns: the object in the range that 
              compared equal to the parameter, 
              or None if no such object exists.
    """
    return where(lambda elem: elem == object, iterable)


