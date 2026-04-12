
from typing import Callable

import traceback

"""
global list to collect all methods marked @unit_test.
"""
__test_methods__: list[Callable[..., None]] = list()
__test_errors__: list[tuple[Callable, Exception, str]] = list()


class TestFailedError(Exception):
    """
    exception to be raised if a unit-test fails.
    """
    pass



class UnitTest:
    """
    unit-test utility-methods.
    """


    def assert_eq(a, b) -> None:
        """
        :raises TestFailedError: if a != b.
        """
        if (a != b):
            raise TestFailedError(f"'{repr(a)}' was not equal to '{repr(b)}'")


    def assert_neq(a, b) -> None:
        """
        :raises TestFailedError: if a == b.
        """
        if (a == b):
            raise TestFailedError(f"'{repr(a)}' was equal to '{repr(b)}'")



def unit_test(func: Callable[[], None]):
    """
    function-decorator to enqueue a function
    for unit-testing. 
    
    the marked function will be added
    to a list of test-methods, that will all be try-excepted
    as soon as unit_test.run() is called.
    """
    def __inner__(*args, **kwargs) -> None:
        try:
            func(*args, **kwargs)
            print(f"unit-test of {func.__qualname__} ..... PASSED")
        except Exception as e:
            print(f"unit-test of {func.__qualname__} ..... FAILED")
            __test_errors__.append((func, e, traceback.format_exc()))
    __test_methods__.append(__inner__)
    return __inner__


def run() -> None:
    """
    runs all functions marked with @unit_test.
    """
    print("----------[ UNIT-TESTS ]----------")
    print(f"running {len(__test_methods__)} unit-tests .....")
    print("---------- ------------ ----------")
    for __method__ in __test_methods__:
        __method__()
    print("---------- ------------ ----------")
    print(f"results: {len(__test_methods__) - len(__test_errors__)} / {len(__test_methods__)} unit-tests successful")
    if (len(__test_errors__) != 0):
        print("errors: ")
        for func, e, tb in __test_errors__:
            print(f">>> {func.__qualname__}, raised error: {type(e).__name__} : {str(e)}")
            print(tb)
    print("---------- ------------ ----------")