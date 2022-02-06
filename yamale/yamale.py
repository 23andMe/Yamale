#!/usr/bin/env python
from typing import Any, List

from yamale.schema.validationresults import ValidationResult
from .schema import Schema
from .yamale_error import YamaleError


def make_schema(path: str=None, parser: str='PyYAML', validators=None, content: str=None, encoding: str='utf-8') -> Schema:
    """
    Reads YAML schemas from files or a string.
    :param path: Path to the schema file or directory.
    :param parser: Parser to use. Can be 'PyYAML' or 'ruamel'.
    :param validators: List of validators to use.
    :param content: Content of the YAML schema. If not provided, the schema is read from `path`.
    :param encoding: Encoding of the YAML schema files. Only used if `path` is provided.
    """
    # validators = None means use default.
    # Import readers here so we can get version information in setup.py.
    from . import readers
    raw_schemas = readers.parse_yaml(path, parser, content=content, encoding=encoding)
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
        raise SyntaxError(error)

    return s


def make_data(path: str=None, parser: str='PyYAML', content: str=None, encoding: str='utf-8'):
    """
    Reads a YAML file containing the data.
    :param path: Path to the YAML file or directory.
    :param parser: Parser to use. Can be 'PyYAML' or 'ruamel'.
    :param content: Content of the YAML file. If not provided, the data is read from `path`.
    :param encoding: Encoding of the YAML files. Only used if `path` is provided.
    :return: A list of parsed YAML files. The object types depend on the parser used.
    """
    from . import readers
    raw_data = readers.parse_yaml(path, parser, content=content, encoding=encoding)
    if len(raw_data) == 0:
        return [({}, path)]
    return [(d, path) for d in raw_data]


def validate(schema: Schema, data: List[Any], strict: bool=True, _raise_error: bool=True) -> List[ValidationResult]:
    """
    Validates the list of YAML files against the schema.
    :param schema: Schema to validate against.
    :param data: List of YAML files to validate.
    :param strict: If True, unexpected elements in the data will cause validation errors.
    :param _raise_error: If True, raises an exception if a validation error occurs.
    """
    results: List[ValidationResult] = []
    is_valid = True
    for d, path in data:
        result = schema.validate(d, path, strict)
        results.append(result)
        is_valid = is_valid and result.isValid()
    if _raise_error and not is_valid:
        raise YamaleError(results)
    return results
