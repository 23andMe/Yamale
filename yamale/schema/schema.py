import sys
from .. import syntax, util
from .. import validators as val

# Fix Python 2.x.
PY2 = sys.version_info[0] == 2


class Schema(object):
    """
    Makes a Schema object from a schema dict.
    Still acts like a dict.
    """
    def __init__(self, schema_dict, name='', validators=None):
        self.validators = validators or val.DefaultValidators
        self.dict = schema_dict
        self.name = name
        self._schema = self._process_schema(schema_dict, self.validators)
        self.includes = {}

    def add_include(self, type_dict):
        for include_name, custom_type in type_dict.items():
            t = Schema(custom_type, name=include_name,
                       validators=self.validators)
            self.includes[include_name] = t

    def __getitem__(self, key):
        return self._schema[key]

    def _process_schema(self, schema_dict, validators):
        """
        Go through a schema and construct validators.
        """
        schema_flat = util.flatten(schema_dict)

        for key, expression in schema_flat.items():
            try:
                schema_flat[key] = syntax.parse(expression, validators)
            except SyntaxError as e:
                # Tack on some more context and rethrow.
                error = str(e) + ' at node \'%s\'' % key
                raise SyntaxError(error)
        return schema_flat

    def validate(self, data):
        errors = []

        for key, validator in self._schema.items():
            errors += self._validate(validator, data, key=key, includes=self.includes)

        if errors:
            header = '\nError validating data %s with schema %s' % (data.name, self.name)
            error_str = header + '\n\t' + '\n\t'.join(errors)
            if PY2:
                error_str = error_str.encode('utf-8')
            raise ValueError(error_str)

    def _validate(self, validator, data, key, position=None, includes=None):
        """
        Run through a schema and a data structure,
        validating along the way.

        Ignores fields that are in the data structure, but not in the schema.

        Returns an array of errors.
        """
        errors = []

        if position:
            position = '%s.%s' % (position, key)
        else:
            position = key

        try:  # Pull value out of data. Data can be a map or a list/sequence
            data_item = util.get_value(data, key)
        except KeyError:  # Oops, that field didn't exist.
            if validator.is_optional:  # Optional? Who cares.
                return errors
            # SHUT DOWN EVERTYHING
            errors.append('%s: Required field missing' % position)
            return errors

        return self._validate_item(validator, data_item, position, includes)

    def _validate_item(self, validator, data_item, position, includes):
        """
        Validates a single data item against validator.

        Returns an array of errors.
        """
        errors = []

        # Optional field with optional value? Who cares.
        if data_item is None and validator.is_optional and validator.can_be_none:
            return errors

        errors += self._validate_primitive(validator, data_item, position)

        if errors:
            return errors

        if isinstance(validator, val.Include):
            errors += self._validate_include(validator, data_item,
                                             includes, position)

        elif isinstance(validator, (val.Map, val.List)):
            errors += self._validate_map_list(validator, data_item,
                                              includes, position)

        elif isinstance(validator, val.Any):
            errors += self._validate_any(validator, data_item,
                                         includes, position)

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

        for key, validator in include_schema._schema.items():
            errors += include_schema._validate(validator, data, includes=includes, key=key, position=pos)

        return errors

    def _validate_any(self, validator, data, includes, pos):
        errors = []

        if not validator.validators:
            errors.append('No validators specified for "any".')
            return errors

        sub_errors = []
        for v in validator.validators:
            err = self._validate_item(v, data, pos, includes)
            if err:
                sub_errors.append(err)

        if len(sub_errors) == len(validator.validators):
            # All validators failed, add to errors
            for err in sub_errors:
                errors += err

        return errors

    def _validate_primitive(self, validator, data, pos):
        errors = validator.validate(data)

        for i, error in enumerate(errors):
            errors[i] = '%s: ' % pos + error

        return errors
