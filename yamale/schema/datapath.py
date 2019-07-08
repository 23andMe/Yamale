from operator import getitem
from functools import reduce
from ..util import isstr
# ABCs for containers were moved to their own module
try:
    from collections.abc import Mapping, Iterable
except ImportError:
    from collections import Mapping, Iterable


def paths(data):
    items = _getitems(data)
    if not items:
        return [DataPath()]

    return [DataPath(key) + subpath
            for key, subdata in items
            for subpath in paths(subdata)]


def _getitems(obj):
    if isinstance(obj, Mapping):
        return obj.items()
    if isinstance(obj, Iterable) and not isstr(obj):
        return enumerate(obj)


class DataPath(object):

    def __init__(self, *path):
        self._path = path

    def __add__(self, other):
        dp = DataPath()
        dp._path = self._path + other._path
        return dp

    def __str__(self):
        return '.'.join(map(str, (self._path)))

    def __repr__(self):
        return 'DataPath({})'.format(repr(self._path))

    def getitem(self, data):
        return reduce(getitem, self._path, data)
