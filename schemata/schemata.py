#!/usr/bin/env python
import readers
from schema import Schema
from data import Data


def schema(path):
    raw_schemas = readers.parse_file(path)
    schema = Schema(raw_schemas[0], path)
    for raw_schema in raw_schemas[1:]:
        schema.add(Schema(raw_schema), path)
    return schema


def data(path):
    raw_data = readers.parse_file(path)
    return Data(raw_data, path)


def validate(schema, *data):
    for d in data:
        schema.validate(d)
    return data
