#!/usr/bin/env python
import sys
import os
from .schema import Schema

PY2 = sys.version_info[0] == 2


def make_schema(path, parser='PyYAML', validators=None):
    # validators = None means use default.
    # test if the schema.yaml file is empty
    try:
        if not os.path.getsize(path):
            raise ValueError('schema.yaml is an empty file!')
    except ValueError as e:
        print(e)
        raise ValueError(e)
    # Import readers here so we can get version information in setup.py.
    from . import readers
    raw_schemas = readers.parse_file(path, parser)

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
    return [(d, path) for d in raw_data]


def validate(schema, data, strict=False):
    for d, path in data:
        schema.validate(d, path, strict)
    return data
