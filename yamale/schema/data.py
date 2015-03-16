from . import util
from operator import getitem

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

    def __setitem__(self, key, value):
        super(Data, self).__setitem__(key, value)
        path, key = util.get_expanded_path(self.dict, key)
        util.reduce(getitem, path, self.dict)[key] = value

    def __delitem__(self, key, value):
        super(Data, self).__setitem__(key, value)
        path, key = util.get_expanded_path(self.dict, key)
        del util.reduce(getitem, path, self.dict)[key]
