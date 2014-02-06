class Validator(object):
    """Base class for all Validators"""
    __constraints__ = []

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        self.is_required = bool(kwargs.get('required', True))

        self.__tag__ = getattr(self, '__tag__', self.__class__)

        fail = '\'%s\' ' + 'is not a %s.' % self.get_name()
        self.__fail__ = getattr(self, '__fail__', fail)

        self.constraints = []
        for constraint in self.__constraints__:
            self.constraints.append(constraint(kwargs))

    @property
    def is_optional(self):
        return not self.is_required

    def get_name(self):
        return self.__tag__

    def is_valid(self, value):
        """
        Check if ``value`` is valid.

        :returns: [errors] If ``value`` is invalid, otherwise [].
        """
        errors = []

        for constraint in self.constraints:
            error = constraint.is_valid(value)
            if error:
                errors.append(error)

        valid = self._is_valid(value)
        if not valid:
            errors.append(self._fail(value))

        return errors

    def _is_valid(self, value):
        raise NotImplemented

    def _fail(self, value):
        return self.__fail__ % value

    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.args, self.kwargs)

    def __eq__(self, other):
        eq = [isinstance(other, self.__class__),
              self.args == other.args,
              self.kwargs == other.kwargs]
        return all(eq)
