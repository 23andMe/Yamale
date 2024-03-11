# -*- coding: utf-8 -*-

from yamale.validators.base import Validator


class OneOf(Validator):
    """One of given values validator"""
    tag = 'oneof'

    def __init__(self, *args, **kwargs):
        super(OneOf, self).__init__(*args, **kwargs)
        self.values = args

    def _is_valid(self, value):
        return value in self.values

    def fail(self, value):
        return '\'%s\' is not in %s' % (value, self.values)
