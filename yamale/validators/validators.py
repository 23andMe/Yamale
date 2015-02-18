from collections import Set, Sequence, Mapping
from .base import Validator
from . import constraints as con


# Python 3 has no basestring, lets test it.
try:
    basestring  # attempt to evaluate basestring
    def isstr(s):
        return isinstance(s, basestring)
except NameError:
    def isstr(s):
        return isinstance(s, str)


class String(Validator):
    """String validator"""
    tag = 'str'
    constraints = [con.LengthMin, con.LengthMax, con.CharacterExclude]

    def _is_valid(self, value):
        return isstr(value)


class Number(Validator):
    """Number/float validator"""
    tag = 'num'
    constraints = [con.Min, con.Max]

    def _is_valid(self, value):
        return isinstance(value, (int, float))


class Integer(Validator):
    """Integer validator"""
    tag = 'int'
    constraints = [con.Min, con.Max]

    def _is_valid(self, value):
        return isinstance(value, int)


class Boolean(Validator):
    """Boolean validator"""
    tag = 'bool'

    def _is_valid(self, value):
        return isinstance(value, bool)


class Enum(Validator):
    """Enum validator"""
    tag = 'enum'

    def __init__(self, *args, **kwargs):
        super(Enum, self).__init__(*args, **kwargs)
        self.enums = args

    def _is_valid(self, value):
        return value in self.enums

    def fail(self, value):
        return '\'%s\' not in %s' % (value, self.enums)


class Map(Validator):
    """Map and dict validator"""
    tag = 'map'

    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        self.validators = [val for val in args if isinstance(val, Validator)]

    def _is_valid(self, value):
        return isinstance(value, Mapping)


class List(Validator):
    """List validator"""
    tag = 'list'

    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
        self.validators = [val for val in args if isinstance(val, Validator)]

    def _is_valid(self, value):
        return isinstance(value, (Set, Sequence)) and not isstr(value)


class Include(Validator):
    """Include validator"""
    tag = 'include'

    def __init__(self, *args, **kwargs):
        self.include_name = args[0]
        super(Include, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        return isinstance(value, Mapping)

    def get_name(self):
        return self.include_name


DefaultValidators = {}

for v in Validator.__subclasses__():
    # Allow validator nodes to contain either tags or actual name
    DefaultValidators[v.tag] = v
    DefaultValidators[v.__name__] = v
