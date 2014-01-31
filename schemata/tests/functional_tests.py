from nose.tools import raises

from . import get_fixture
from schemata import schema, data, validate
from .. import validators as val

TYPES = get_fixture('types.yaml')
TYPES_GOOD = get_fixture('types_good_data.yaml')
TYPES_BAD = get_fixture('types_bad_data.yaml')

NESTED = get_fixture('nested.yaml')
NESTED_GOOD = get_fixture('nested_good_data.yaml')
NESTED_BAD = get_fixture('nested_bad_data.yaml')

KEYWORDS = get_fixture('keywords.yaml')

CUSTOM = get_fixture('custom_types.yaml')
CUSTOM_GOOD = get_fixture('custom_types_good.yaml')


def test_tests():
    ''' Make sure the test runner is working.'''
    assert 1 + 1 == 2


def test_flat_schema():
    types_schema = schema(TYPES)
    assert isinstance(types_schema['string'], val.String)


def test_flat_validate():
    types_schema = schema(TYPES)
    types_good = data(TYPES_GOOD)
    assert validate(types_schema, types_good)


@raises(ValueError)
def test_bad_validate():
    types_schema = schema(TYPES)
    types_bad = data(TYPES_BAD)
    validate(types_schema, types_bad)


def test_nested_schema():
    nested_schema = schema(NESTED)
    assert isinstance(nested_schema['string'], val.String)
    assert isinstance(nested_schema['list'], (list, tuple))
    assert isinstance(nested_schema['list'][0], val.String)


def test_nested_validate():
    nested_schema = schema(NESTED)
    nested_good_data = data(NESTED_GOOD)
    assert validate(nested_schema, nested_good_data)


@raises(ValueError)
def test_bad_nested():
    nested_schema = schema(NESTED)
    nested_bad_data = data(NESTED_BAD)
    validate(nested_schema, nested_bad_data)


def test_custom():
    custom = schema(CUSTOM)
    custom_good = data(CUSTOM_GOOD)
    assert validate(custom, custom_good)
