from .. import syntax
from . import util


class Schema(dict):
    """
    Makes a Schema object from a schema dict.
    Still acts like a dict. #NeverGrowUp
    """
    def __init__(self, schema_dict, name=''):
        flat_schema = util.flatten(schema_dict)
        self._process_schema_dict(flat_schema)
        dict.__init__(self, flat_schema)
        self.dict = schema_dict
        self.name = name
        self.custom_types = {}

    def add_type(self, type_schema):
        self.custom_types[type_schema.keys()[0]] = type_schema

    def _process_schema_dict(self, flat_schema):
        '''
        Warning: this method mutates input.

        Go through a flat schema dict and construct validators.
        '''
        for key, expression in flat_schema.items():
            flat_schema[key] = syntax.parse(expression)

    def validate(self, data):
        try:
            self._validate(self, data)
        except ValueError, e:
            raise ValueError('\nError validating data %s with schema %s. %s' % (data.name, self.name, e.message))

    def _validate(self, schema, data):
        '''
        Recursively run through a schema and a data structure,
        validating along the way.

        Ignores fields that are in the data structure, but not in the schema.
        '''
        for pos, validator in schema.items():
            if not validator.is_valid(data[pos]):
                raise ValueError(
                    '\n\nFailed validation at %s:\n\t\t%s should be a %s.' %
                    (pos, data[pos], validator.__class__.__name__))
