import pytest
from hw3.curry import curry_explicit, uncurry_explicit


def test_curry_basic():
    """Test basic currying with multiple arguments"""

    def add(a, b, c):
        return a + b + c

    curried = curry_explicit(add, 3)
    assert curried(1)(2)(3) == 6


def test_curry_single_arity():
    """Test currying with single arity"""

    def double(x):
        return x * 2

    curried = curry_explicit(double, 1)
    assert curried(5) == 10


def test_curry_zero_arity():
    """Test currying with zero arity"""

    def constant():
        return 42

    curried = curry_explicit(constant, 0)
    assert curried() == 42


def test_curry_negative_arity():
    """Test that negative arity raises ValueError"""

    def func(x):
        return x

    with pytest.raises(ValueError, match="Arity cannot be negative"):
        curry_explicit(func, -1)


def test_uncurry_basic():
    """Test basic uncurrying"""

    def curried_add(a):
        return lambda b: lambda c: a + b + c

    uncurried = uncurry_explicit(curried_add, 3)
    assert uncurried(1, 2, 3) == 6


def test_uncurry_single_arity():
    """Test uncurrying with single arity"""

    def curried_double(x):
        return x * 2

    uncurried = uncurry_explicit(curried_double, 1)
    assert uncurried(5) == 10


def test_uncurry_wrong_arguments_number():
    """Test that wrong number of arguments raises error"""

    def curried_func(a):
        return lambda b: a + b

    uncurried = uncurry_explicit(curried_func, 2)

    with pytest.raises(ValueError, match="Expected 2 arguments, got 1"):
        uncurried(1)


def test_curry_uncurry():
    """Test that currying and uncurrying are inverses"""

    def original(a, b, c):
        return a * b * c

    curried = curry_explicit(original, 3)
    uncurried = uncurry_explicit(curried, 3)

    assert uncurried(2, 3, 4) == original(2, 3, 4)


def test_builtin_functions():
    """Test currying with built-in functions"""

    curried_abs = curry_explicit(abs, 1)
    assert curried_abs(-5) == 5
    assert curried_abs(10) == 10

    curried_pow = curry_explicit(pow, 2)
    power_of_2 = curried_pow(2)
    assert curried_pow(2)(3) == 8
    assert curried_pow(3)(3) == 27


def test_functions_with_arbitrary_arity():
    """Test currying with functions that have arbitrary arity"""

    curried_max = curry_explicit(max, 2)
    assert curried_max(3)(5) == 5
    assert curried_max(7)(20) == 20

    curried_min = curry_explicit(min, 3)
    assert curried_min(-1)(5)(3) == -1
    assert curried_min(-2)(-5)(0) == -5


def test_one_at_the_time():
    "Test that curried functions take one argument at the time"

    f = curry_explicit((lambda x, y, z: f"<{x},{y},{z}>"), 3)

    assert f(123)(456)(562) == "<123,456,562>"

    with pytest.raises(TypeError, match="takes 1 positional argument but 2 were given"):
        f(123, 456)(562)

    with pytest.raises(TypeError, match="takes 1 positional argument but 3 were given"):
        f(123, 456, 562)
