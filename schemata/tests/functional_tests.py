from . import get_fixture
from schemata import schema, data, validate
from .. import validators as val

TYPES = get_fixture('types.yaml')
TYPES_GOOD = get_fixture('types_good_data.yaml')
KEYWORDS = get_fixture('keywords.yaml')

types_schema = schema(TYPES)


def test_tests():
    ''' Make sure the test runner is working.'''
    assert 1 + 1 == 2


def test_schema():
    assert isinstance(types_schema['string'], val.String)


def test_validate():
    assert validate(types_schema, TYPES_GOOD)


# def test_types():
#     t = yaml.parse_file(TYPES)
#     assert isinstance(t['string'], String)
#     assert isinstance(t['number'], Number)
#     assert isinstance(t['boolean'], Boolean)
#     assert isinstance(t['integer'], Integer)


# def test_keywords():
#     t = yaml.parse_file(KEYWORDS)
#     assert t['optional'].is_optional
#     assert t['min'].is_required
#     assert '?str' not in t['optional'].args
#     assert t['optional_min'].min == 1
#     for arg in t['optional_min'].args:
#         assert '=' not in arg
#     assert t['default'].default is True
#     assert t['max'].max == 100
