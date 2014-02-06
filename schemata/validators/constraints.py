class Constraint(object):
    """docstring for Constraint"""
    __kwargs__ = {}

    def __init__(self, kwargs):
        print kwargs
        self._parseKwargs(kwargs)

    def _parseKwargs(self, kwargs):
        for kwarg, ktype in self.__kwarg__.items():
            value = self.get_kwarg(kwargs, kwarg, ktype)
            setattr(self, kwarg, value)

    def get_kwarg(self, kwargs, key, ktype, default=None):
        try:
            return ktype(kwargs.get(key))
        except TypeError:
            return default

    def is_valid(self, value):
        try:
            if not self._is_valid(value):
                return self._fail(value)
        except TypeError, e:
            return e.message
        return None

    def _fail(self, value):
        return '\'%s\' violates %s.' % (value, self.__class__.__name__)


class Min(Constraint):
    __kwarg__ = {'min': float}
    fail = '%s is less than than %s'

    def _is_valid(self, value):
        return self.min <= value

    def _fail(self, value):
        return self.fail % (value, self.min)


class Max(Constraint):
    __kwarg__ = {'max': float}
    fail = '%s is greater than %s'

    def _is_valid(self, value):
        return self.max >= value

    def _fail(self, value):
        return self.fail % (value, self.max)


class LengthMin(Constraint):
    __kwarg__ = {'min': int}
    fail = 'Length of %s is less than than %s'

    def _is_valid(self, value):
        return self.min <= len(value)

    def _fail(self, value):
        return self.fail % (value, self.min)


class LengthMax(Constraint):
    __kwarg__ = {'max': int}
    fail = 'Length of %s is greater than %s'

    def _is_valid(self, value):
        return self.max >= len(value)

    def _fail(self, value):
        return self.fail % (value, self.max)
