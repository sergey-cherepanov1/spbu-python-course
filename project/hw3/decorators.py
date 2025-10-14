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


def smart_args(*, pos_args: bool = False) -> Callable[..., Any]:
    """
    Decorator for smart argument handling with Evaluated and Isolated types.

    Args:
        pos_args: Whether to handle positional arguments with smart defaults.

    Returns:
        A decorator that wraps a given function.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        spec = inspect.getfullargspec(func)

        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            def_kwargs = spec.kwonlydefaults
            if def_kwargs:
                for k in def_kwargs:

                    if (
                        type(def_kwargs[k]) == Evaluated
                        and def_kwargs[k].func == Isolated
                    ):
                        assert False, "Cannot combine Evaluated and Isolated"

                    if type(def_kwargs[k]) == Evaluated and k not in kwargs:
                        kwargs[k] = def_kwargs[k].func()
                    elif type(def_kwargs[k]) == Isolated:
                        if k in kwargs:
                            kwargs[k] = copy.deepcopy(kwargs[k])
                        else:
                            raise ValueError(
                                "A keyword argument with default value Isolated was not passed."
                            )
            if pos_args:
                args_l = list(args)
                spec_args = list(spec.args)
                spec_defaults = list(spec.defaults) if spec.defaults else []
                start = len(args_l) - (len(spec_args) - len(spec_defaults))

                for i in range(start, len(spec_defaults)):
                    if isinstance(spec_defaults[i], Evaluated) and isinstance(
                        spec_defaults[i].func, Isolated
                    ):
                        assert False, "Cannot combine Evaluated and Isolated"

                    if isinstance(spec_defaults[i], Evaluated):
                        args_l.append(spec_defaults[i].func())
                    elif isinstance(spec_defaults[i], Isolated):
                        raise ValueError(
                            "A positional argument with default value Isolated was not passed."
                        )
                    else:
                        args_l.append(spec_defaults[i])

                shift = len(spec_args) - len(spec_defaults)
                for i in range(start):
                    if isinstance(spec_defaults[i], Isolated):
                        args_l[shift + i] = copy.deepcopy(args_l[shift + i])
                args = tuple(args_l)

            return func(*args, **kwargs)

        return inner

    return decorator
    
    
def cache(*, capacity: int = 0) -> Callable[..., Any]:
    """
    Decorator for caching function results.

    Args:
        capacity: Maximum number of results to cache. If 0, caching is disabled.

    Returns:
        A decorator that wraps a given function.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        cache_dict: OrderedDict = OrderedDict()

        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            if capacity <= 0:
                return func(*args, **kwargs)
            try:
                key = hash((args, tuple(sorted(kwargs.items()))))
            except TypeError:
                return func(*args, **kwargs)

            if key in cache_dict:
                cache_dict.move_to_end(key)
                return cache_dict[key]

            if len(cache_dict) == capacity:
                cache_dict.popitem(last=False)

            cache_dict[key] = func(*args, **kwargs)
            return cache_dict[key]

        return inner

    return decorator
