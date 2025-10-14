"""
This module provides explicit currying and uncurrying functions which allow
converting between normal functions and their curried versions with
specified arity.
"""

import functools
from typing import Any, Callable


def curry_explicit(func: Callable[..., Any], arity: int) -> Callable[..., Any]:
    """
    Convert a function into its curried version with explicit arity.

    Args:
        func: The function to be curried.
        arity: The number of arguments the function expects.

    Returns:
        A curried version of the function.

    Raises:
        ValueError: If arity is negative.
    """

    if arity < 0:
        raise ValueError("Arity cannot be negative.")
    if arity == 0:
        return func

    @functools.wraps(func)
    def curried(arg):
        if arity == 1:
            return func(arg)
        return curry_explicit(lambda *args: func(arg, *args), arity - 1)

    return curried


def uncurry_explicit(func: Callable[..., Any], arity: int) -> Callable[..., Any]:
    """
    Convert a curried function back to it's normal form with explicit arity.

    Args:
        func: The curried function to be uncurried
        arity: The number of arguments the original function expected

    Returns:
        An uncurried version of the function.

    Raises:
        ValueError: If arity is negative or wrong number of arguments provided.
    """

    if arity < 0:
        raise ValueError("Arity cannot be negative.")

    @functools.wraps(func)
    def uncurried(*args):
        if len(args) != arity:
            raise ValueError(f"Expected {arity} arguments, got {len(args)}")

        result = func
        for arg in args:
            result = result(arg)
        return result

    return uncurried
