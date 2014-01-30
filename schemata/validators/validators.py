from .base import Validator, MinMixin, MaxMixin


class String(MinMixin, MaxMixin, Validator):
    """String validator"""
    __tag__ = 'str'

    def __init__(self, *args, **kwargs):
        super(String, self).__init__(*args, **kwargs)

    def is_valid(self, value):
        return isinstance(value, basestring)


class Number(MinMixin, MaxMixin, Validator):
    """Number/float validator"""
    __tag__ = 'num'

    def __init__(self, *args, **kwargs):
        super(Number, self).__init__(*args, **kwargs)

    def is_valid(self, value):
        return isinstance(value, float) or isinstance(value, int)


class Integer(MinMixin, MaxMixin, Validator):
    """Integer validator"""
    __tag__ = 'int'

    def __init__(self, *args, **kwargs):
        super(Integer, self).__init__(*args, **kwargs)

    def is_valid(self, value):
        return isinstance(value, int)


class Boolean(Validator):
    """Boolean validator"""
    __tag__ = 'bool'

    def __init__(self, *args, **kwargs):
        super(Boolean, self).__init__(*args, **kwargs)

    def is_valid(self, value):
        return isinstance(value, bool)


class List(Validator):
    """List validator"""
    __tag__ = 'list'

    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)

    def is_valid(self, value):
        return isinstance(value, list)
