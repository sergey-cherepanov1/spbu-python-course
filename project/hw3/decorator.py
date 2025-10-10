"""
Decorator for smart argument handling and caching.
"""

from functools import wraps
from collections import OrderedDict
from typing import Any, Callable, Optional, Dict
import copy


class Evaluated:
    """A wrapper for dynamically evaluated default values.

    Args:
        func: A function that returns the default value.
    """

    def __init__(self, func: Callable[..., Any]) -> None:
        self.func = func


class Isolated:
    """A marker for arguments that should be deep-copied before use."""

    pass


def smart_args(capacity: int = 0) -> Callable[..., Any]:
    """
    Decorator for caching function results with smart argument handling.

    Args:
        capacity: Maximum number of results to cache. If 0, caching is disabled.

    Returns:
        A decorator that wraps a given function.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        cache: OrderedDict = OrderedDict()

        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            def_kwargs = func.__kwdefaults__
            if def_kwargs:
                for k in def_kwargs:
                    if type(def_kwargs[k]) == Evaluated:
                        kwargs[k] = def_kwargs[k].func()
                    elif type(def_kwargs[k]) == Isolated:
                        kwargs[k] = copy.deepcopy(kwargs[k])

            if capacity <= 0:
                return func(*args, **kwargs)
            try:
                key = hash((args, tuple(sorted(kwargs.items()))))
            except TypeError:
                return func(*args, **kwargs)

            if key in cache:
                cache.move_to_end(key)
                print(cache)
                return cache[key]
            if len(cache) == capacity:
                cache.popitem(last=False)

            cache[key] = func(*args, **kwargs)
            return cache[key]

        return inner

    return decorator
