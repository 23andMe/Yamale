#!/usr/bin/env python
from readers import yaml
import syntax
import validators


def schema(path):
    schema = {}
    raw_schema = yaml.parse_file(path)
    for k in walk_dict(raw_schema):
        schema[k] = syntax.parse(raw_schema[k])
    return schema


def data(path):
    return yaml.parse_file(path)


def validate(schema, data):
    return True
    return validators.validate(schema, data)


def walk_dict(dic):
    for key in dic.keys():
        yield key
