import sys

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

    def add_type(self, type_dict):
        for custom_name, custom_type in type_dict.items():
            t = Schema(custom_type, name=custom_name)
            self.custom_types[custom_name] = t

    def _process_schema(self, schema):
        '''
        Warning: this method mutates input.

        Go through a schema and construct validators.
        '''
        for key, expression in schema.items():
            try:
                schema[key] = syntax.parse(expression)
            except SyntaxError, e:
                raise SyntaxError(e.message + ' at \'%s\'' % key)

    def validate(self, data):
        try:
            self._validate(data, custom_types=self.custom_types)
        except ValueError, e:
            raise ValueError('\nError validating data %s with schema %s\n %s'
                             % (data.name, self.name, e.message)), None, sys.exc_info()[2]

    def _validate(self, data, custom_types=None, prefix=''):
        '''
        Run through a schema and a data structure,
        validating along the way.

        Ignores fields that are in the data structure, but not in the schema.
        '''
        for pos, validator in self.items():
            try:
                pos = prefix + pos
                if isinstance(validator, val.Include) and data[pos]:
                    t = validator.type
                    custom_types[t]._validate(data, custom_types=custom_types, prefix=pos + '.')

                elif not validator.is_valid(data[pos]):
                    raise ValueError(
                        '\nFailed validation at %s:\n\t\t\'%s\' is not a %s.' %
                        (pos, data[pos], validator.__tag__)), None, sys.exc_info()[2]

            except KeyError:
                if validator.is_optional:
                    continue
                raise ValueError(
                    '\nFailed validation at %s:\n\t\tRequired field missing.' %
                    pos), None, sys.exc_info()[2]
