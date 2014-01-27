class Validator(object):
    """Base class for all Validators"""
    def __init__(self, arg):
        super(Validator, self).__init__()
        self.arg = arg
