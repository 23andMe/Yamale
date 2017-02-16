#!/usr/bin/env python
import sys
from .schema import Schema
from .schema import Data

PY2 = sys.version_info[0] == 2


def make_schema(path, validators=None):
    # validators = None means use default.
    # Import readers here so we can get version information in setup.py.
    from . import readers
    raw_schemas = readers.parse_file(path)

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


def make_data(path):
    from . import readers
    raw_data = readers.parse_file(path)
    return [Data(d, path) for d in raw_data]


def validate(schema, data):
    for d in data:
        schema.validate(d)
    return data
