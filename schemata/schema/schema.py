import sys

from .. import syntax
from . import util
from .data import Data
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
        self.includes = {}

    def add_include(self, type_dict):
        for include_name, custom_type in type_dict.items():
            t = Schema(custom_type, name=include_name)
            self.includes[include_name] = t

    def _process_schema(self, schema):
        '''
        Warning: this method mutates input.

        Go through a schema and construct validators.
        '''
        for key, expression in schema.items():
            try:
                schema[key] = syntax.parse(expression)
            except SyntaxError, e:
                # Tack on some more context and rethrow.
                raise SyntaxError(e.message + ' at \'%s\'' % key)

    def validate(self, data):
        try:
            for pos, validator in self.items():
                self._validate(validator, data, position=pos, includes=self.includes)
        except ValueError, e:
            # Tack on some more context and rethrow.
            raise ValueError('\nError validating data %s with schema %s\n %s'
                             % (data.name, self.name, e.message)), None, sys.exc_info()[2]

    def _validate(self, validator, data, position='', includes=None):
        '''
        Run through a schema and a data structure,
        validating along the way.

        Ignores fields that are in the data structure, but not in the schema.
        '''
        try:  # Pull value out of data. Data can be a map or a list/sequence
            data_item = data[position]
        except KeyError:  # Oops, that field didn't exist.
            if validator.is_optional:  # Optional? Who cares.
                return
            # SHUT DOWN EVERTYHING
            self._validate_fail(position, 'Required field missing: %s' % position)

        self._validate_primitive(validator, data_item, position)

        if isinstance(validator, val.Include):
            self._validate_include(validator, data_item, includes, position)

        elif isinstance(validator, val.List):
            self._validate_list(validator, data_item, includes, position)

    def _validate_list(self, validator, data, includes, position):
        if not validator.validators:
            return  # No validators, user just wanted a list.

        passed = [False] * len(data)

        for i, d in enumerate(data):
            for v in validator.validators:
                try:
                    self._validate(v, data, i, includes)
                except ValueError:
                    # Validation failed, try the next one
                    continue
                passed[i] = True
                break

        if not all(passed):
            bad_val = str(data[passed.index(False)])
            vals = ' or '.join([v.__tag__ for v in validator.validators])
            self._validate_fail(position, '%s not valid for %s' % (bad_val, vals))

    def _validate_include(self, validator, data, includes, position):
        include_schema = includes.get(validator.include_name)
        if not include_schema:
            self._validate_fail(position, 'Include \'%s\' has not been defined.' % validator.include_name)

        for pos, validator in include_schema.items():
            include_schema._validate(validator, data, includes=includes, position=pos)

    def _validate_primitive(self, validator, data, position):
        if not validator.is_valid(data):
            self._validate_fail(position, '%s\' is not a %s.' % (data, validator.__tag__))

    def _validate_fail(self, position, msg):
        raise ValueError('\nFailed validation at %s:\n\t\t%s' % (position, msg)), None, sys.exc_info()[2]

