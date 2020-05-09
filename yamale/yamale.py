#!/usr/bin/env python
import sys
import os
from .schema import Schema
from .yamale_error import YamaleError

PY2 = sys.version_info[0] == 2


def make_schema(path, parser='PyYAML', validators=None):
    # validators = None means use default.
    # Import readers here so we can get version information in setup.py.
    from . import readers
    raw_schemas = readers.parse_file(path, parser)
    if not raw_schemas:
        raise ValueError('{} is an empty file!'.format(path))
    # First document is the base schema
    try:
        s = Schema(raw_schemas[0], path, validators=validators)
        # Additional documents contain Includes.
        for raw_schema in raw_schemas[1:]:
            s.add_include(raw_schema)
    except (TypeError, SyntaxError) as e:
        error = 'Schema error in file %s\n' % path
        error += str(e)
        if PY2:
            error.encode('utf-8')
        raise SyntaxError(error)

    return s


def make_data(path, parser='PyYAML'):
    from . import readers
    raw_data = readers.parse_file(path, parser)
    if len(raw_data) == 0:
        return [({}, path)]
    return [(d, path) for d in raw_data]


def validate(schema, data, strict=False, _raise_error=True):
    results = []
    is_valid = True
    for d, path in data:
        result = schema.validate(d, path, strict)
        results.append(result)
        is_valid = is_valid and result.isValid()
    if _raise_error and not is_valid:
        raise YamaleError(results)
    return results
