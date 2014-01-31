from .. import syntax
from . import util
from schemata import validators as val


class Schema(dict):
    """
    Makes a Schema object from a schema dict.
    Still acts like a dict. #NeverGrowUp
    """
    def __init__(self, schema_dict, name=''):
        schema = util.flatten(schema_dict)
        dict.__init__(self, schema)
        self._process_schema(self)
        self.dict = schema_dict
        self.name = name
        self.custom_types = {}

    def add_type(self, type_schema):
        self.custom_types[type_schema.keys()[0]] = type_schema

    def _process_schema(self, schema):
        '''
        Warning: this method mutates input.

        Go through a schema and construct validators.
        '''
        for key, expression in schema.items():
            schema[key] = syntax.parse(expression)

    def validate(self, data):
        try:
            self._validate(self, data)
        except ValueError, e:
            raise ValueError('\nError validating data %s with schema %s\n %s' % (data.name, self.name, e.message))

    def _validate(self, schema, data, prefix=''):
        '''
        Run through a schema and a data structure,
        validating along the way.

        Ignores fields that are in the data structure, but not in the schema.
        '''
        for pos, validator in schema.items():
            try:

                if isinstance(validator, val.Include):
                    t = validator.type
                    print t
                    self.custom_types[t].validate(data, prefix=pos)

                if not validator.is_valid(data[prefix + pos]):
                    raise ValueError(
                        '\nFailed validation at %s:\n\t\t%s should be a %s.' %
                        (pos, data[pos], validator.__class__.__name__))

            except KeyError:
                if validator.is_optional:
                    continue
                raise ValueError(
                    '\nFailed validation at %s:\n\t\t%s not found.' %
                    (pos, validator.__class__.__name__))
