"""
This script is for measure purpose.
"""
import time
from functools import wraps
from memory_profiler import memory_usage


def profile(func):
    """
    function measure time and memory usage for specific method.
    :param func: function
    :return: print the result
    """
    @wraps(func)
    def inner(*args, **kwargs):
        fn_kwargs_str = ', '.join(f'{k}={v}' for k, v in kwargs.items())
        print(f'\n{func.__name__}({fn_kwargs_str})')

        # Measure time
        time_count = time.perf_counter()
        retval = func(*args, **kwargs)
        elapsed = time.perf_counter() - time_count
        print(f'Time   {elapsed:0.4}')

        # Measure memory
        mem, retval = memory_usage((func, args, kwargs),
                                   retval=True, timeout=200, interval=1e-7)

        print(f'Memory {max(mem) - min(mem)}')
        return retval

    return inner
