"""
Decorator for smart argument handling and caching.
"""

from functools import wraps
from collections import OrderedDict
from typing import Any, Callable, Dict
import copy, inspect


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


def smart_args(*, capacity: int = 0, pos_args: bool = False) -> Callable[..., Any]:
    """
    Decorator for caching function results with smart argument handling.

    Args:
        capacity: Maximum number of results to cache. If 0, caching is disabled.

    Returns:
        A decorator that wraps a given function.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        cache: OrderedDict = OrderedDict()
        spec = inspect.getfullargspec(func)

        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            def_kwargs = spec.kwonlydefaults
            if def_kwargs:
                for k in def_kwargs:

                    if type(def_kwargs[k]) == Evaluated and def_kwargs[k].func == Isolated:
                        assert False, "Cannot combine Evaluated and Isolated"
                        
                    if type(def_kwargs[k]) == Evaluated and k not in kwargs:
                        kwargs[k] = def_kwargs[k].func()
                    elif type(def_kwargs[k]) == Isolated and kwargs[k]:
                        kwargs[k] = copy.deepcopy(kwargs[k])
                        
            def_args = spec.defaults
            if (pos_args and def_args):
                args = list(args)
                for a in range(len(def_args)):
                    index = a + (len(args) - len(def_args))
                    
                    if type(def_args[a]) == Evaluated and def_args[a].func == Isolated:
                        assert False, "Cannot combine Evaluated and Isolated"
                    
                    if type(def_args[a]) == Evaluated:
                        try:
                            args[index] = def_args[a].func()
                        except:
                            print("A positional argument with default value Evaluated was not passed.")
                            raise
                            
                    elif type(def_args[a]) == Isolated:
                        try:
                            args[index] = copy.deepcopy(args[index])
                        except IndexError:
                            print("A positional argument with default value Isolated was not passed.")
                            raise
            
            if capacity <= 0:
                return func(*args, **kwargs)
            
            try:
                key = hash((tuple(args), tuple(sorted(kwargs.items()))))
            except TypeError:
                return func(*args, **kwargs)

            if key in cache:
                cache.move_to_end(key)
                return cache[key]
            
            if len(cache) == capacity:
                cache.popitem(last=False)

            cache[key] = func(*args, **kwargs)
            return cache[key]

        return inner

    return decorator
    
