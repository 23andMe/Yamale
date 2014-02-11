from . import util


class Data(dict):
    """
    Makes a Data object from a data dict.
    Still acts like a dict.

    Takes a name so it can be identified, like in exceptions.
    """
    def __init__(self, data_dict, name=''):
        flat_data = util.flatten(data_dict, keep_iter=True)
        dict.__init__(self, flat_data)
        self.name = name
        self.dict = data_dict
