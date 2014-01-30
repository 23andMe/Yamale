class Data(dict):
    """
    Makes a Data object from a data dict.
    Still acts like a dict. #NeverGrowUp

    Takes a name so it can be identified.
    """
    def __init__(self, data_dict, name=''):
        dict.__init__(self, data_dict)
        self.name = name
