import pytest
from collections import OrderedDict
from typing import Dict, List
from hw3.decorators import smart_args, cache, Evaluated, Isolated


def test_basic_caching():
    """Test that basic caching works with same arguments"""
    call_count = 0

    @cache(capacity=2)
    def f(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    assert f(5) == 10
    assert call_count == 1

    assert f(5) == 10
    assert call_count == 1


def test_cache_capacity():
    """Test for cache capacity limits"""
    call_count = 0

    @cache(capacity=2)
    def f(x):
        nonlocal call_count
        call_count += 1
        return x

    f(1)
    f(2)
    f(3)

    f(1)
    assert call_count == 4


def test_evaluated_kwargs():
    """Test Evaluated default value for keyword arguments"""

    l = (i for i in range(2))

    def generator():
        return next(l)

    @smart_args()
    def check_evaluation(*, evl=Evaluated(generator)):
        return evl

    assert check_evaluation() == 0
    assert check_evaluation() == 1
    assert check_evaluation(evl=100) == 100


def test_isolated_kwargs():
    """Test Isolated default value for keyword arguments"""

    @smart_args()
    def check_isolation(*, d=Isolated()):
        d["a"] = 0
        return d

    no_mutable = {"a": 10}
    assert check_isolation(d=no_mutable) == {"a": 0}


def test_evaluated_positional_args():
    """Test Evaluated defaults with positional arguments"""
    counter = 0

    def check_evaluation():
        nonlocal counter
        counter += 1
        return counter

    @smart_args(pos_args=True)
    def f(a=Evaluated(check_evaluation)):
        return a

    assert f() == 1
    assert f() == 2


def test_isolated_positional_args():
    """Test Isolated default value for positional arguments"""

    @smart_args(pos_args=True)
    def f(a=Isolated()):
        a.append(5555)
        return a

    l = [1, 2, 3]

    assert f(l) == [1, 2, 3, 5555]
    assert l == [1, 2, 3]


def test_isolated_without_argument():
    """Test that Isolated requires argument to be passed"""

    @smart_args()
    def requires_isolated(*, data=Isolated()):
        return data

    with pytest.raises(
        ValueError,
        match="A keyword argument with default value Isolated was not passed",
    ):
        requires_isolated()


def test_error_evaluated_isolated_conflict():
    """Test error when both Evaluated and Isolated are used on same argument"""

    @smart_args()
    def conflicting_args(*, arg=Evaluated(Isolated)):
        return arg

    with pytest.raises(AssertionError, match="Cannot combine Evaluated and Isolated"):
        conflicting_args()


def test_complex_mixed_arguments():
    """Test with multiple positional and keyword mixed types"""
    counter_1 = 0
    counter_2 = 0

    def check_evaluation_1():
        nonlocal counter_1
        counter_1 += 1
        return counter_1

    def check_evaluation_2():
        nonlocal counter_2
        counter_2 += 1
        return counter_2

    @cache(capacity=5)
    @smart_args(pos_args=True)
    def complex_func(
        a=Isolated(),
        b=Evaluated(check_evaluation_1),
        *,
        x=Evaluated(check_evaluation_2),
        y=Isolated(),
    ):

        a.append(f"changed_{b}")
        y["new"] = f"changed_{x}"
        return a, y

    args = [1, 2]
    kws = {"a": 0}

    result_a, result_y = complex_func(args, y=kws)
    assert result_a == [1, 2, "changed_1"]
    assert result_y == {"a": 0, "new": "changed_1"}
    assert args == [1, 2]
    assert kws == {"a": 0}

    result_a2, result_y2 = complex_func(args, y=kws)
    assert result_a2 == [1, 2, "changed_2"]
    assert result_y2 == {"a": 0, "new": "changed_2"}

def test_not_every_arg_defaulted():
    """Test functions with args that dont have default values"""
    
    @smart_args(pos_args=True)
    def f(pos1, pos2=Isolated(), *, kw1, kw2=Evaluated(lambda: "!!!")):
        pos2.append(pos1)
        return {
            'pos1': pos1,
            'pos2': pos2,
            'kw1': kw1,
            'kw2': kw2
        }
    
    isolated = ["a"]
    
    result = f(10, isolated, kw1=5)
    assert result['pos1'] == 10
    assert result['pos2'] == ["a", 10]
    assert isolated == ["a"]
    assert result['kw1'] == 5
    assert result['kw2'] == "!!!"
