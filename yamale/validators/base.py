class Validator(object):
    """Base class for all Validators"""

    constraints = []
    value_type = None

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        # Is field required? Default is True
        self.is_required = bool(kwargs.pop("required", True))

        # Can value be None if field is optional? Default is True
        self._value_can_be_none = bool(kwargs.pop("none", True))

        # Construct all constraints
        self._constraints_inst = self._create_constraints(self.constraints, self.value_type, kwargs)

    def _create_constraints(self, constraint_classes, value_type, kwargs):
        from . import constraints as con
        import itertools
        from .. import util

        universal_constraints = []
        for constraint in util.get_subclasses(con.Constraint):
            if constraint.universal:
                universal_constraints.append( constraint )

        constraints = []
        for constraint in itertools.chain( constraint_classes, universal_constraints ):
            constraints.append(constraint(value_type, kwargs))
        return constraints

    @property
    def tag(self):
        return self.__class__

    @property
    def is_optional(self):
        return not self.is_required

    @property
    def can_be_none(self):
        """Check if value for optional field can be None."""
        return self._value_can_be_none

    def _is_valid(self, value):
        """Validators must implement this. Return True if value is valid."""
        raise NotImplementedError("You need to override this function")

    def get_name(self):
        return self.tag

    def validate(self, value, path=None):
        """
        Check if ``value`` is valid.

        :returns: [errors] If ``value`` is invalid, otherwise [].
        """
        errors = []

        # Make sure pre_check constraints validates first.
        for constraint in self._constraints_inst:
            if constraint.pre_check:
                if hasattr( constraint, '_is_valid_path' ):
                  error = constraint.is_valid_path(path)

                if hasattr( constraint, '_is_valid' ):
                  error = constraint.is_valid(value)

                if error:
                    if isinstance(error, list):
                        errors.extend(error)
                    else:
                        errors.append(error)
                    return errors

        valid = self._is_valid(value)
        if not valid:
            errors.append(self.fail(value))
            return errors

        # Then validate all the constraints second.
        for constraint in self._constraints_inst:
            if hasattr( constraint, '_is_valid_path' ):
              error = constraint.is_valid_path(path)

            if hasattr( constraint, '_is_valid' ):
              error = constraint.is_valid(value)

            if error:
                if isinstance(error, list):
                    errors.extend(error)
                else:
                    errors.append(error)

        return errors

    def is_valid(self, value):
        return self.validate(value) == []

    def fail(self, value):
        """Override to define a custom fail message"""
        return "'%s' is not a %s." % (value, self.get_name())

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.args, self.kwargs)

    def __eq__(self, other):
        # Validators are equal if they have the same args and kwargs.
        eq = [isinstance(other, self.__class__), self.args == other.args, self.kwargs == other.kwargs]
        return all(eq)
