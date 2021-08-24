import itertools

__all__ = ['permutations']


def permutations(options):
    return sum(
        map(
            lambda i: list(map(lambda t: [t], itertools.permutations(options, i))),
            range(1, len(options) + 1)
        ), start=[]
    )
