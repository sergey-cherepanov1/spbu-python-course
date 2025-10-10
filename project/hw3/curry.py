"""

"""

import functools, inspect

def curry_explicit(func, arity):
    if  arity < 0:
        raise ValueError("Arity cannot be negative.")

    @functools.wraps(func)
    def curried(*args, **kwargs):
        args_count = len(args) + len(kwargs)
        
        if args_count > arity:
            raise ValueError(f"Too many arguments. Expected {arity}, given {args_count}.")
        
        if args_count == arity:
            return func(*args, **kwargs)
        else:
            return lambda *args1, **kwargs1: curried(*args, *args1, **kwargs, **kwargs1)
    
    return curried

def uncurry_explicit(func, arity):
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


f2 = curry_explicit((lambda x, y, z: f'<{x},{y}, {z}>'), 3)
g2 = uncurry_explicit(f2, 3)
print(f2(123)(456)(562))
print(g2(123, 456, 562))
