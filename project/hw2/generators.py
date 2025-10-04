"""
Implementation of a Lazy Stream Processing System Using Generators
"""
from typing import Iterable, Callable, Any, Iterator
from functools import reduce

def generate(iterable: Iterable[Any]) -> Iterator[Any]:
    """
    Creates a generator that yields each item from the input iterable.
    
    Args:
        iterable: Any iterable object.
        
    Yields:
        Items from the input iterable.
    """
    
    for it in iterable:
        yield it

def collect(data: Iterator[Any], collector: Callable[[Iterable[Any]], Any]=list) -> Any:
    """
    Collects all items from the iterator into a container, using the given collector function.
    
    Args:
        data: The iterator whose items will be collected.
        collector: A function which is used to produces a collection.

    Returns:
        The collected items.
    """
    
    return collector(data)
        
def convey(
    data: Iterable[Any], 
    operations: Iterable[tuple[Callable[..., Any], tuple[Any], dict[str, Any]]]
    ) -> Iterator[Any]:
    """
    Applies given operations to given data.
    
    Args:
        data: Given container of data.
        operations: An iterable of tuples (function, args, kwargs).
        
    Returns:
        Iterator after all operations are applied.
    """
    
    generator = generate(data)
    for op in operations:
        prepared_func = unify_func(*op)
        generator = prepared_func(generator)
        
    return generator
        
   
def unify_func(f: Callable[..., Any], *args: Any, **kwargs: Any) -> Callable[[Iterable[Any]], Iterator[Any]]:
    """
    Wraps a function so it can process iterable data.
    
    Args:
        f: The function to be applied.
        *args: Positional arguments for the function.
        **kwargs: Keyword arguments for the function.
        
    Returns:
        Unified function which can be applied to any iterable object.
    """
    
    if f in [map, filter, zip, enumerate]:
        return lambda it: f(*args, it, **kwargs)
    elif f == reduce:
        if len(args) == 2:
            return lambda it: iter([f(args[0], it, args[1],**kwargs)])
        else:
            return lambda it: iter([f(*args, it, **kwargs)])
    else:
        return lambda it: f(it, *args, **kwargs)
