from typing import Callable
import cProfile
import pstats


def profile_deco(function: Callable):
    profile = cProfile.Profile()

    def wrapper(*args, **kwargs):
        profile.enable()
        result = function(*args, **kwargs)
        profile.disable()
        return result

    def print_stat():
        ps = pstats.Stats(profile).sort_stats("cumulative").strip_dirs()
        ps.print_stats()

    wrapper.print_stat = print_stat

    return wrapper


@profile_deco
def add(a: int, b: int):
    return a + b


@profile_deco
def sub(a: int, b: int):
    return a - b


if __name__ == "__main__":
    add(1, 2)
    add(4, 5)
    sub(4, 5)

    add.print_stat()
    sub.print_stat()
