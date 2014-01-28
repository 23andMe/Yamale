from .base import Validator, MinMixin, MaxMixin


def to_bool(b):
    return b in ['true', '1', 't', 'y', 'yes', 'True']


class String(MinMixin, MaxMixin, Validator):
    """String validator"""
    __tag__ = 'str'

    def __init__(self, *args, **kwargs):
        super(String, self).__init__(*args, **kwargs)

    def validate(self):
        return isinstance(self.min, unicode)


class Number(MinMixin, MaxMixin, Validator):
    """Number/float validator"""
    __tag__ = 'num'

    def __init__(self, *args, **kwargs):
        super(Number, self).__init__(*args, **kwargs)


class Integer(MinMixin, MaxMixin, Validator):
    """Integer validator"""
    __tag__ = 'int'

    def __init__(self, *args, **kwargs):
        super(Integer, self).__init__(*args, **kwargs)


class Boolean(Validator):
    """Boolean validator"""
    __tag__ = 'bool'

    def __init__(self, *args, **kwargs):
        super(Boolean, self).__init__(*args, **kwargs)
        self.default = to_bool(kwargs.get('default'))


class List(Validator):
    """List validator"""
    __tag__ = 'list'

    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
