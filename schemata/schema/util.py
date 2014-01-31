def flatten(dic, keep_lists=False):
    '''
    Returns a flattened dictionary from a dictionary of nested dictionaries and lists.
    `keep_lists` will treat lists as valid values, while also flattening them.
    '''
    return {pos: val for (pos, val) in walk(dic, keep_lists=keep_lists)}


def walk(dic, position='', keep_lists=False):
    i = get_iter(dic)

    for key, value in i:
        pos = '%s.%s' % (position, key)
        pos = pos.lstrip('.')

        if keep_lists and isinstance(value, list):
            yield pos, value

        if is_iter(value):
            for tup in walk(value, pos):
                yield tup
        else:
            yield pos, value


def is_iter(obj):
    return isinstance(obj, dict) or isinstance(obj, list)


def get_iter(iterable):
    if isinstance(iterable, list):
        return enumerate(iterable)
    else:
        return iterable.items()
