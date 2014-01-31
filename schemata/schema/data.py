from . import util


class Data(dict):
    """
    Makes a Data object from a data dict.
    Still acts like a dict. #NeverGrowUp

    Takes a name so it can be identified.
    """
    def __init__(self, data_dict, name=''):
        flat_data = util.flatten(data_dict, keep_lists=True)
        dict.__init__(self, flat_data)
        self.name = name
        self.dict = data_dict
