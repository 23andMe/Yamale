from collections import Set, Sequence, Mapping
from .base import Validator
from . import constraints as con


class String(Validator):
    """String validator"""
    __tag__ = 'str'
    __constraints__ = [con.LengthMin, con.LengthMax]

    def _is_valid(self, value):
        return isinstance(value, basestring)


class Number(Validator):
    """Number/float validator"""
    __tag__ = 'num'
    __constraints__ = [con.Min, con.Max]

    def _is_valid(self, value):
        return isinstance(value, (int, float))


class Integer(Validator):
    """Integer validator"""
    __tag__ = 'int'
    __constraints__ = [con.Min, con.Max]

    def _is_valid(self, value):
        return isinstance(value, int)


class Boolean(Validator):
    """Boolean validator"""
    __tag__ = 'bool'

    def _is_valid(self, value):
        return isinstance(value, bool)


class Enum(Validator):
    """Enum validator"""
    __tag__ = 'enum'

    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
        self.enums = args

    def _is_valid(self, value):
        return value in self.enums

    def _fail(self, value):
        return '\'%s\' not in %s' % (value, self.enums)


class List(Validator):
    """List validator"""
    __tag__ = 'list'

    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
        self.validators = [val for val in args if isinstance(val, Validator)]

    def _is_valid(self, value):
        return isinstance(value, (Set, Sequence)) and not isinstance(value, basestring)


class Include(Validator):
    """Include validator"""
    __tag__ = 'include'

    def __init__(self, *args, **kwargs):
        self.include_name = args[0]
        super(Include, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        return isinstance(value, Mapping)

    def get_name(self):
        return self.include_name
