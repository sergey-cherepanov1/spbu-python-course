import pytest
from hw3.curry import curry_explicit, uncurry_explicit

def test_curry_basic():
    """Test basic currying with multiple arguments"""
    def add(a, b, c):
        return a + b + c
    
    curried = curry_explicit(add, 3)
    assert curried(1)(2)(3) == 6
    assert curried(1, 2)(3) == 6
    assert curried(1, 2, 3) == 6

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

def test_curry_too_many_arguments():
    """Test that too many arguments raises error"""
    def func(x, y):
        return x + y
    
    curried = curry_explicit(func, 2)
    
    with pytest.raises(ValueError, match="Too many arguments"):
        curried(1)(2, 3)

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
