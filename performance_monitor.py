
import cProfile
import pstats

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