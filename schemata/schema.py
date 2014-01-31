import syntax


class Schema(dict):
    """
    Makes a Schema object from a schema dict.
    Still acts like a dict. #NeverGrowUp
    """
    def __init__(self, schema_dict, name=''):
        self._process_schema_dict(schema_dict)
        dict.__init__(self, schema_dict)
        self.name = name

    def _is_dict(self, obj):
        return isinstance(obj, dict)

    def _is_list(self, obj):
        return isinstance(obj, list)

    def _is_iter(self, iterable):
        return self._is_list(iterable) or self._is_dict(iterable)

    def _get_iter(self, iterable):
        if self._is_list(iterable):
            return enumerate(iterable)
        else:
            return iterable.items()

    def _process_schema_dict(self, schema):
        '''
        Warning: this method mutates input.

        Recursively go through a raw schema dict and construct validators.
        '''
        i = self._get_iter(schema)

        for key, value in i:
            if self._is_dict(value) or self._is_list(value):
                self._process_schema_dict(value)
            else:
                schema[key] = syntax.parse(value)

    def validate(self, data):
        try:
            self._validate(self, data, [])
        except ValueError, e:
            raise ValueError('Error validating %s: ' % data.name + e.message)

    def _validate(self, schema, data, position):
        '''
        Recursively run through a schema and a data structure,
        validating along the way.

        Ignores fields that are in the data structure, but not in the schema.
        '''
        i = self._get_iter(schema)

        for key, validator in i:
            if self._is_iter(validator):
                self._validate(validator, data[key], position + [key])
            else:
                if not validator.is_valid(data[key]):
                    raise ValueError("Validation failed at " + str(position + [key]))
