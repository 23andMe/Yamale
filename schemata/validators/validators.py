from collections import Set, Sequence, Mapping
from .base import Validator, MinMixin, MaxMixin

# Always include mixins first, then the Validator base class.


class String(MinMixin, MaxMixin, Validator):
    """String validator"""
    __tag__ = 'str'

    def is_valid(self, value):
        return isinstance(value, basestring)


class Number(MinMixin, MaxMixin, Validator):
    """Number/float validator"""
    __tag__ = 'num'

    def is_valid(self, value):
        return isinstance(value, float) or isinstance(value, int)


class Integer(MinMixin, MaxMixin, Validator):
    """Integer validator"""
    __tag__ = 'int'

    def is_valid(self, value):
        return isinstance(value, int)


class Boolean(Validator):
    """Boolean validator"""
    __tag__ = 'bool'

    def is_valid(self, value):
        return isinstance(value, bool)


class List(Validator):
    """List validator"""
    __tag__ = 'list'

    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
        self.validators = [val for val in args if isinstance(val, Validator)]

    def is_valid(self, value):
        return isinstance(value, (Set, Sequence)) and not isinstance(value, basestring)


class Include(Validator):
    """Include validator"""
    __tag__ = 'include'

    def __init__(self, *args, **kwargs):
        super(Include, self).__init__(*args, **kwargs)
        self.include_name = args[0]

    def is_valid(self, value):
        return isinstance(value, Mapping)

    def get_name(self):
        return self.include_name
