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
        self.custom_validators = {}

    def add_include(self, type_dict):
        for include_name, custom_type in type_dict.items():
            if custom_type==None:
                raise SyntaxError('{}: no custom type or validator found\nThis error may be caused by the use of tabulations'.format(include_name))
            if isinstance(custom_type, str): # custom_type is a validator
                try:
                    self.custom_validators[include_name] = syntax.parse(custom_type, self.validators)
                except SyntaxError as e:
                    # Tack on some more context and rethrow.
                    error = str(e) + ' at node \'%s\'' % key
                    raise SyntaxError(error)
            else:
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
            errors += self._validate(validator, data, key=key, includes=self.includes, custom_validators=self.custom_validators)

        if errors:
            header = '\nError validating data %s with schema %s' % (data.name, self.name)
            error_str = header + '\n\t' + '\n\t'.join(errors)
            if PY2:
                error_str = error_str.encode('utf-8')
            raise ValueError(error_str)

    def _validate(self, validator, data, key, includes=None, custom_validators=None, position=None):
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

        return self._validate_item(validator, data_item, includes, custom_validators, position)

    def _validate_item(self, validator, data_item, includes, custom_validators, position):
        """
        Validates a single data item against validator.

        Returns an array of errors.
        """
        errors = []

        if data_item is None and validator.is_optional:  # Optional? Who cares.
            return errors

        errors += self._validate_primitive(validator, data_item, position)

        if errors:
            return errors

        if isinstance(validator, val.Include):
            errors += self._validate_include(validator, data_item,
                                             includes, custom_validators, position)

        elif isinstance(validator, (val.Map, val.List)):
            errors += self._validate_map_list(validator, data_item,
                                              includes, custom_validators, position)

        elif isinstance(validator, val.Any):
            errors += self._validate_any(validator, data_item,
                                         includes, custom_validators, position)

        return errors

    def _validate_map_list(self, validator, data, includes, custom_validators, pos):
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
                if isinstance(v, val.Include): # Include validator
                    if not v.args[0] in custom_validators.keys() and isinstance(data[key], dict):
                        err = self._validate(v, data, key, includes=includes, custom_validators=custom_validators, position=pos)
                    elif v.args[0] in custom_validators.keys():
                        err = self._validate(custom_validators[v.args[0]], data, key, includes=includes, custom_validators=custom_validators, position=pos)
                    else:
                        err = ["{}.{}: '{}' is not a {}".format(pos, key, data[key], v.args[0])]
                    
                else:
                    err = self._validate(v, data, key, includes=includes, custom_validators=custom_validators, position=pos)
                if err:
                    sub_errors.append(err)

            if len(sub_errors) == len(validator.validators):
                # All validators failed, add to errors
                for err in sub_errors:
                    errors += err

        return errors

    def _validate_include(self, validator, data, includes, custom_validators, pos):
        errors = []

        include_schema = includes.get(validator.include_name)
        if not include_schema:
            # The included object may be a custom validator
            include_validator = custom_validators.get(validator.include_name)
            if not include_validator:
                errors.append('Include \'%s\' has not been defined.' % validator.include_name)
                return errors
            errors += self._validate_item(include_validator, data, includes, custom_validators, pos)
        else:
            for key, validator in include_schema._schema.items():
                errors += include_schema._validate(validator, data, key, includes=includes, custom_validators=custom_validators, position=pos)

        return errors

    def _validate_any(self, validator, data, includes, custom_validators, pos):
        errors = []

        if not validator.validators:
            errors.append('No validators specified for "any".')
            return errors

        sub_errors = []
        for v in validator.validators:
            if isinstance(v, val.Include): # Included validator or node
                if not v.args[0] in custom_validators.keys() and isinstance(data, dict):
                    err = self._validate_item(v, data, includes, custom_validators, pos)
                elif v.args[0] in custom_validators.keys():
                    err = self._validate_item(custom_validators[v.args[0]], data, includes, custom_validators, pos)
                else:
                    err = ["{}: '{}' is not a {}".format(pos, data, v.args[0])]
                    
            else:
                err = self._validate_item(v, data, includes, custom_validators, pos)
            if err:
                sub_errors.append(err)

        if len(sub_errors) == len(validator.validators):
            # All validators failed, add to errors
            for err in sub_errors:
                errors += err

        return errors

    def _validate_primitive(self, validator, data, pos):
        # print(validator, data, pos)
        if isinstance(validator, val.Include):
            if validator.args[0] in self.custom_validators.keys():
                return []
        errors = validator.validate(data)

        for i, error in enumerate(errors):
            errors[i] = '%s: ' % pos + error

        return errors
