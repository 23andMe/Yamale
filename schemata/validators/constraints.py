class Constraint(object):
    """docstring for Constraint"""
    __kwargs__ = {}
    is_active = True

    def __init__(self, kwargs):
        self._parseKwargs(kwargs)

    def _parseKwargs(self, kwargs):
        for kwarg, ktype in self.__kwarg__.items():
            value = self.get_kwarg(kwargs, kwarg, ktype)
            setattr(self, kwarg, value)

    def get_kwarg(self, kwargs, key, ktype, default=None):
        value = kwargs.get(key)

        # Deactivate this constraint if no value was found.
        if value is None:
            self.is_active = False
            return value

        try:
            return ktype(kwargs.get(key))
        except ValueError:
            raise SyntaxError('%s is not a %s' % (key, ktype))

    def is_valid(self, value):
        if not self.is_active:
            return None

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
