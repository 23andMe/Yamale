from .. import syntax
from . import util
from .. import validators as val


class Schema(dict):
    """
    Makes a Schema object from a schema dict.
    Still acts like a dict.
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
            except SyntaxError as e:
                # Tack on some more context and rethrow.
                raise SyntaxError(str(e) + ' at node \'%s\'' % key)

    def validate(self, data):
        errors = []

        for key, validator in self.items():
            errors += self._validate(validator, data, key=key, includes=self.includes)

        if errors:
            header = '\nError validating data %s with schema %s' % (data.name, self.name)
            error_str = '\n\t' + '\n\t'.join(errors)
            raise ValueError(header + error_str)

    def _validate(self, validator, data, key, position=None, includes=None):
        '''
        Run through a schema and a data structure,
        validating along the way.

        Ignores fields that are in the data structure, but not in the schema.

        Returns an array of errors.
        '''
        errors = []

        if position:
            position = '%s.%s' % (position, key)
        else:
            position = key

        try:  # Pull value out of data. Data can be a map or a list/sequence
            data_item = data[key]
        except KeyError:  # Oops, that field didn't exist.
            if validator.is_optional:  # Optional? Who cares.
                return errors
            # SHUT DOWN EVERTYHING
            errors.append('%s: Required field missing' % position)
            return errors

        # If we don't need it, we don't care if it's not there.
        if data_item is None and validator.is_optional:
            return errors

        errors += self._validate_primitive(validator, data_item, position)

        if errors:
            return errors

        if isinstance(validator, val.Include):
            errors += self._validate_include(validator, data_item, includes, position)

        elif isinstance(validator, (val.Map, val.List)):
            errors += self._validate_map_list(validator, data_item, includes, position)

        return errors


    def _validate_map_list(self, validator, data, includes, pos):
        errors = []

        if not validator.validators:
            return errors  # No validators, user just wanted a map.

        if isinstance(validator, val.List):
            keys = range(len(data))
        else:
            keys = data.keys()

        for key in keys:
            sub_errors = []
            for v in validator.validators:
                err = self._validate(v, data, key, pos, includes)
                if err:
                    sub_errors.append(err)

            if len(sub_errors) == len(validator.validators):
                # All validators failed, add to errors
                for err in sub_errors:
                    errors += err

        return errors


    def _validate_include(self, validator, data, includes, pos):
        errors = []

        include_schema = includes.get(validator.include_name)
        if not include_schema:
            errors.append('Include \'%s\' has not been defined.' % validator.include_name)
            return errors

        for key, validator in include_schema.items():
            errors += include_schema._validate(validator, data, includes=includes, key=key, position=pos)

        return errors

    def _validate_primitive(self, validator, data, pos):
        errors = validator.validate(data)

        for i, error in enumerate(errors):
            errors[i] = '%s: ' % pos + error

        return errors


