class ValidationError(ValueError):
    """A value is invalid for a given validator"""


class Validator(object):
    """Base class for all Validators"""
    def __init__(self, *args, **kwargs):
        super(Validator, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.is_required = bool(kwargs.get('required', True))
        self.is_optional = not self.is_required

    def is_valid(self, value):
        """Check if ``value`` is valid.

        :returns: False If ``value`` is invalid, otherwise True.
        """
        raise NotImplementedError

    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.args, self.kwargs)

    def __eq__(self, other):
        eq = [isinstance(other, self.__class__),
              set(self.args) == set(other.args),
              self.kwargs == other.kwargs]
        return all(eq)


def get_kwarg(kwargs, key, type, default=None):
    try:
        return type(kwargs.get(key))
    except TypeError:
        return default


class MinMixin(object):
    """docstring for MinMixin"""
    def __init__(self, *arg, **kwargs):
        super(MinMixin, self).__init__(*arg, **kwargs)
        self.min = get_kwarg(kwargs, 'min', int)


class MaxMixin(object):
    """docstring for MinMixin"""
    def __init__(self, *arg, **kwargs):
        super(MaxMixin, self).__init__(*arg, **kwargs)
        self.max = get_kwarg(kwargs, 'max', int)

