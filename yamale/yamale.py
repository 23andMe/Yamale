#!/usr/bin/env python
from .schema import Schema
from .schema import Data


def make_schema(path):
    from . import readers  # Import readers here in case you don't want to use the dependencies.
    raw_schemas = readers.parse_file(path)

    # First document is the base schema
    s = Schema(raw_schemas[0], path)

    # Additional documents contain Includes.
    for raw_schema in raw_schemas[1:]:
        s.add_include(raw_schema)

    return s


def make_data(path):
    from . import readers
    raw_data = readers.parse_file(path)
    return [Data(d, path) for d in raw_data]


def validate(schema, data):
    for d in data:
        schema.validate(d)
    return data
