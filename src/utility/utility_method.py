from itertools import islice


def chunk(lst: list, n: int):
    it = iter(lst)
    return iter(lambda: tuple(islice(it, n)), ())
