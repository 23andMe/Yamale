# -*- coding: utf-8 -*-

import math
import re
from yamale.validators.base import Validator
from yamale.validators import constraints as con
from yamale import util


class MultipleOf(con.Constraint):
    fail = '%s is not a multiple of %s'

    def __init__(self, value_type, kwargs):
        self.keywords = {'mul': value_type, 'prec': float}
        super(MultipleOf, self).__init__(value_type, kwargs)

    def _is_valid(self, value):
        return value % self.mul <= self.prec

    def _fail(self, value):
        return self.fail % (value, self.min)


class PowerOf(con.Constraint):
    fail = '%s is not a power of %s'

    def __init__(self, value_type, kwargs):
        self.keywords = {'pow': value_type, 'prec': float}
        super(PowerOf, self).__init__(value_type, kwargs)

    def _is_valid(self, value):
        return abs(math.log(value, self.pow) % 1 <= self.prec

    def _fail(self, value):
        return self.fail % (value, self.min)


class ExtendedNumber(Validator):
    """Extended number/float validator"""
    value_type = float
    tag = 'xnum'
    constraints = [con.Min, con.Max, MultipleOf, PowerOf]

    def _is_valid(self, value):
        return isinstance(value, (int, float)) and not isinstance(value, bool)

# OR: yamale.validators.validators.Number.constraints.extend([MultipleOf, PowerOf])


class ExtendedInteger(Validator):
    """Extended integer validator"""
    value_type = int
    tag = 'xint'
    constraints = [con.Min, con.Max, MultipleOf, PowerOf]

    def _is_valid(self, value):
        return isinstance(value, int) and not isinstance(value, bool)

# OR: yamale.validators.validators.Integer.constraints.extend([MultipleOf, PowerOf])


class NumberRegex(Validator):
    """Regular expression validator with number support"""
    tag = 'num_regex'
    _regex_flags = {'ignore_case': re.I, 'multiline': re.M, 'dotall': re.S}

    def __init__(self, *args, **kwargs):
        self.regex_name = kwargs.pop('name', None)

        flags = 0
        for k, v in util.get_iter(self._regex_flags):
            flags |= v if kwargs.pop(k, False) else 0

        self.regexes = [re.compile(arg, flags)
                        for arg in args if util.isstr(arg)]
        super(NumberRegex, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        return any(r.match(str(value)) for r in self.regexes)

    def get_name(self):
        return self.regex_name or self.tag + " match"
