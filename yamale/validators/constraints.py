import datetime


class Constraint(object):
    keywords = {}  # Keywords and types accepted by this constraint
    is_active = False

    def __init__(self, value_type, kwargs):
        self._parseKwargs(kwargs)

    def _parseKwargs(self, kwargs):
        for kwarg, kwtype in self.keywords.items():
            value = self.get_kwarg(kwargs, kwarg, kwtype)
            setattr(self, kwarg, value)

    def get_kwarg(self, kwargs, key, kwtype):
        try:
            value = kwargs[key]
        except KeyError:
            return None

        # Activate this constraint
        self.is_active = True

        if isinstance(value, kwtype):
            # value already correct type, return
            return value

        try:  # Try to convert value
            # Is this value one of the datetime types?
            if kwtype == datetime.date:
                time = datetime.datetime.strptime(value, '%Y-%m-%d')
                return datetime.date(time.year, time.month, time.day)

            if kwtype == datetime.datetime:
                return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

            return kwtype(value)
        except (TypeError, ValueError):
            raise SyntaxError('%s is not a %s' % (key, kwtype))

    def is_valid(self, value):
        if not self.is_active:
            return None

        if not self._is_valid(value):
            return self._fail(value)

        return None

    def _fail(self, value):
        return '\'%s\' violates %s.' % (value, self.__class__.__name__)


class Min(Constraint):
    fail = '%s is less than %s'

    def __init__(self, value_type, kwargs):
        self.keywords = {'min': value_type}
        super(Min, self).__init__(value_type, kwargs)

    def _is_valid(self, value):
        return self.min <= value

    def _fail(self, value):
        return self.fail % (value, self.min)


class Max(Constraint):
    fail = '%s is greater than %s'

    def __init__(self, value_type, kwargs):
        self.keywords = {'max': value_type}
        super(Max, self).__init__(value_type, kwargs)

    def _is_valid(self, value):
        return self.max >= value

    def _fail(self, value):
        return self.fail % (value, self.max)


class LengthMin(Constraint):
    keywords = {'min': int}
    fail = 'Length of %s is less than than %s'

    def _is_valid(self, value):
        return self.min <= len(value)

    def _fail(self, value):
        return self.fail % (value, self.min)


class LengthMax(Constraint):
    keywords = {'max': int}
    fail = 'Length of %s is greater than %s'

    def _is_valid(self, value):
        return self.max >= len(value)

    def _fail(self, value):
        return self.fail % (value, self.max)


class CharacterExclude(Constraint):
    keywords = {'exclude': str}
    fail = '\'%s\' contains excluded character \'%s\''

    def _is_valid(self, value):
        for char in self.exclude:
            if char in value:
                self._failed_char = char
                return False
        return True

    def _fail(self, value):
        return self.fail % (value, self._failed_char)
