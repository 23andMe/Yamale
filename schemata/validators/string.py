# class String(object):
#     """String validator"""
#     def __init__(self, min=None, max=None, regex=None):
#         self.min = min
#         self.max = max
#         self.regex = regex

#     def validate(self):
#         return isinstance(self.s, unicode)

#     def __repr__(self):
#         return 'String(%s)' % self.s


class String(object):
    """String validator"""
    __tag__ = 'str'

    def __init__(self, *args):
        self.min = args
        # self.max = max
        # self.regex = regex

    def validate(self):
        return isinstance(self.min, unicode)

    def __repr__(self):
        return 'String(%s)' % self.min
