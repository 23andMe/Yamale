# def flatten(dic, keep_lists=False):
#     '''
#     Returns a flattened dictionary from a dictionary of nested dictionaries and lists.
#     `keep_lists` will treat lists as valid values, while also flattening them.
#     '''
#     return {pos: val for (pos, val) in walk(dic, keep_lists=keep_lists)}


def walk(dic, position='', keep_lists=False):
    i = get_iter(dic)

    for key, value in i:
        pos = '%s.%s' % (position, key)
        if not position:
            pos = pos.lstrip('.')

        if is_iter(value):
            if keep_lists:
                yield pos, value
            for tup in walk(value, pos):
                yield tup
        else:
            yield pos, value


def flatten(dic, keep_lists=False, pos=None):
    obj = {}

    for k, v in get_iter(dic):
        if pos:
            item_key = '%s.%s' % (pos, k)
        else:
            item_key = '%s' % k

        if is_iter(v):
            obj.update(flatten(dic[k], keep_lists, item_key))
            if keep_lists:
                obj[item_key] = v
        else:
            obj[item_key] = v

    return obj


def is_iter(obj):
    return isinstance(obj, (dict, list, tuple))


def get_iter(iterable):
    if isinstance(iterable, (list, tuple)):
        return enumerate(iterable)
    else:
        return iterable.items()
