#!/usr/bin/env python
from readers import yaml
from schema import Schema


def schema(path):
    raw_schema = yaml.parse_file(path)
    return Schema(raw_schema)


def data(path):
    return yaml.parse_file(path)


def validate(schema, *data):
    for d in data:
        schema.validate(d)
    return data
