#!/usr/bin/env python
from readers import yaml
from schema import Schema
from data import Data


def schema(path):
    raw_schema = yaml.parse_file(path)
    return Schema(raw_schema, path)


def data(path):
    raw_data = yaml.parse_file(path)
    return Data(raw_data, path)


def validate(schema, *data):
    for d in data:
        schema.validate(d)
    return data
