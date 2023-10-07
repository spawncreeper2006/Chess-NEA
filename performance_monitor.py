
import cProfile
import pstats
import time

FILENAME = 'performance.txt'

def log_performance(func):
    
    def timed_func(*args, **kwargs):
        with cProfile.Profile() as profile:
            return_val = func(*args, **kwargs)

        with open(FILENAME, 'w') as f:
            results = pstats.Stats(profile, stream=f)
            results.sort_stats(pstats.SortKey.TIME)
            results.print_stats()

        return return_val
    return timed_func

def show_time(func):
    
    def timed_func(*args, **kwargs):
        start = time.perf_counter()
        return_val = func(*args, **kwargs)
        end = time.perf_counter()
        print (end-start)
        return return_val
    
    return timed_func