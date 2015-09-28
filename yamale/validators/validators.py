from collections import Set, Sequence, Mapping
from datetime import date, datetime
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
    value_type = float
    tag = 'num'
    constraints = [con.Min, con.Max]

    def _is_valid(self, value):
        return isinstance(value, (int, float))


class Integer(Validator):
    """Integer validator"""
    value_type = int
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


class Day(Validator):
    """Day validator. Format: YYYY-MM-DD"""
    value_type = date
    tag = 'day'
    constraints = [con.Min, con.Max]

    def _is_valid(self, value):
        return isinstance(value, date)


class Timestamp(Validator):
    """Timestamp validator. Format: YYYY-MM-DD HH:MM:SS"""
    value_type = datetime
    tag = 'timestamp'
    constraints = [con.Min, con.Max]

    def _is_valid(self, value):
        return isinstance(value, datetime)


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
    constraints = [con.LengthMin, con.LengthMax]

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
        return isinstance(value, Mapping) or isinstance(value, Sequence)

    def get_name(self):
        return self.include_name


class Any(Validator):
    """Any of several types validator"""
    tag = 'any'

    def __init__(self, *args, **kwargs):
        self.validators = [val for val in args if isinstance(val, Validator)]
        super(Any, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        return True


class Null(Validator):
    """Validates null"""
    value_type = None
    tag = 'null'

    def _is_valid(self, value):
        return value is None


DefaultValidators = {}

for v in Validator.__subclasses__():
    # Allow validator nodes to contain either tags or actual name
    DefaultValidators[v.tag] = v
    DefaultValidators[v.__name__] = v
