class ValidationError(ValueError):
    """A value is invalid for a given validator"""


class Validator(object):
    """Base class for all Validators"""
    def __init__(self, *args, **kwargs):
        super(Validator, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.is_required = kwargs.get('required', True)
        self.is_optional = not self.is_required

    def validate(self, value, cast=True):
        """Check if ``value`` is valid and if so cast it.

        :param cast: If False, it indicates that the caller is interested only
            on whether ``value`` is valid, not on casting it to the correct type.
            This is essentially an optimization hint for cases that validation
            can be done more efficiently than type conversion.

        :raises ValidationError: If ``value`` is invalid.
        :returns: The casted value if ``cast`` is True, otherwise anything.
        """
        raise NotImplementedError

    def is_valid(self, value):
        """Check if the value is valid.

        :returns: True if the value is valid, False if invalid.
        """
        try:
            self.validate(value, adapt=False)
            return True
        except ValidationError:
            return False

    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.args, self.kwargs)


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

