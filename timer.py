from functools import wraps
from time import time

def stopwatch(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time() * 1000
        result = func(*args, **kwargs)
        end_time = time() * 1000
        print('Elapsed time: {} ms'.format(end_time-start_time))
        return result
    return wrapper