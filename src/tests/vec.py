
from tests.unit_test import UnitTest, unit_test
from utility.vec import vec, vec2i


class VecTests:
    """
    unit-tests for custom vector-class.
    """


    @unit_test
    def construction() -> None:
        v = vec[int]((2, 3, 4))
        u = vec[int]([2, 3, 4])
        k = vec[int](1, 2)
        t = vec[int](4)
        l = vec[int](v)

        UnitTest.assert_eq(str(v), "[2, 3, 4]")
        UnitTest.assert_eq(str(u), "[2, 3, 4]")
        UnitTest.assert_eq(str(k), "[1, 2]")
        UnitTest.assert_eq(str(l), str(v))
        UnitTest.assert_eq(str(t), "[None, None, None, None]")


    @unit_test
    def equality() -> None:
        v = vec[int](2, 3, 4)
        u = vec[int](2, 3, 4)
        k = vec[int]({1, 8, 7})

        UnitTest.assert_eq(v, u)
        UnitTest.assert_neq(k, u)
        UnitTest.assert_eq(v, (2, 3, 4))
        UnitTest.assert_eq(u, [2, 3, 4])


    @unit_test
    def arithmetic() -> None:
        v = vec2i((2, 3))
        u = vec2i((4, 5))

        UnitTest.assert_eq(v + u, (6, 8))
        UnitTest.assert_eq(u - v, (2, 2))
        UnitTest.assert_eq(u * v, [8, 15])
        UnitTest.assert_eq(abs(vec2i(-1, -4)), (1, 4))


    @unit_test
    def types() -> None:
        v = vec[str]([ "iltam", "sumra" ])

        UnitTest.assert_eq(str(v), "['iltam', 'sumra']")

