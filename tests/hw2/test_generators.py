import pytest
from functools import reduce
from hw2.generators import generate, convey, unify, collect

def custom(data, coeff, degree=2):
    for x in data:
        yield coeff * x ** degree

@pytest.fixture
def simple_input():
    return [1, 2, 3, 4]

@pytest.mark.parametrize("inp, expected", [([1, 2 ,3, 4], [1, 2, 3, 4]), ("Hello, World!", ['H', 'e', 'l', 'l', 'o', ',', ' ', 'W', 'o', 'r', 'l', 'd', '!'])])
def test_generate(inp, expected):
    """ Test the generate function with different input types. """
    assert list(generate(inp)) == expected

@pytest.mark.parametrize("collector,expected", [
    (list, [1, 2, 3, 4]),
    (tuple, (1, 2, 3, 4)),
    (set, {1, 2, 3, 4})
])
def test_collect(simple_input, collector, expected):
    """ Test the collect function with different collection types. """
    gen = generate(simple_input)
    result = collect(gen, collector)
    assert result == expected

@pytest.mark.parametrize(
    "func,args,kwargs,inp,expected",
    [
        (map, (lambda x: x + 1,), {}, [1, 2], [2, 3]),
        (filter, (lambda x: x % 2 == 0,), {}, [1, 2, 3, 4], [2, 4]),
        (zip, ([10, 20],), {}, [1, 2], [(10, 1), (20, 2)]),
        (enumerate, (), {}, ["a", "b"], [(0, "a"), (1, "b")]),
        (reduce, (lambda x, y: x + y,), {}, [1, 2, 3], [6]),
        (reduce, (lambda x, y: x * y, 10), {}, [1, 2, 3], [60]),
        (custom, (5,), {"degree": 0.5}, [1, 4, 9], [5, 10, 15])
    ],
)
def test_unify(func, args, kwargs, inp, expected):
    """ Test the unify function with various built-in and a custom function. """
    unified = unify(func, *args, **kwargs)
    out = list(unified(inp))
    assert out == expected

@pytest.mark.parametrize(
    "operations,expected",
    [
        ([(map, (lambda x: x * 2,), {}), (filter, (lambda x: x > 4,), {})], [6, 8]),
        ([(filter, (lambda x: x < 3,), {})], [1, 2]),
        ([(reduce, (lambda x, y: x + y,), {})], [10]),
        ([(custom, (3,), {"degree": 2}), (reduce, (lambda x, y: (-x) + y, 5,), {})], [35])
    ]
)
def test_convey(simple_input, operations, expected):
    """ Test the convey function by chaining multiple operations on generated data. """
    out = convey(generate(simple_input), operations)
    assert list(out) == expected
