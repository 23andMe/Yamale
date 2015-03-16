from collections import Mapping, Set, Sequence

# Python 3 has no basestring, lets test it.
try:
    basestring  # attempt to evaluate basestring

    def isstr(s):
        return isinstance(s, basestring)
except NameError:
    def isstr(s):
        return isinstance(s, str)


def flatten(dic, keep_iter=False, position=None):
    """
    Returns a flattened dictionary from a dictionary of nested dictionaries and lists.
    `keep_iter` will treat iterables as valid values, while also flattening them.
    """
    child = {}

    for k, v in get_iter(dic):
        if isstr(k):
            k = k.replace('.', '_')
        if position:
            item_position = '%s.%s' % (position, k)
        else:
            item_position = '%s' % k

        if is_iter(v):
            child.update(flatten(dic[k], keep_iter, item_position))
            if keep_iter:
                child[item_position] = v
        else:
            child[item_position] = v

    return child


def is_iter(obj):
    # Strings are not iterables for our use case.
    if isstr(obj):
        return False
    # Is it list like?
    if isinstance(obj, (Sequence, Set)):
        return True
    # A dictionary, perhaps?
    if isinstance(obj, Mapping):
        return True
    # lol, nope
    return False


def get_iter(iterable):
    if isinstance(iterable, Mapping):
        return iterable.items()
    else:
        return enumerate(iterable)
