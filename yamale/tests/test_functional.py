from . import get_fixture
import yamale
from .. import validators as val

types = {
    'schema': 'types.yaml',
    'bad': 'types_bad_data.yaml',
    'good': 'types_good_data.yaml'
}

nested = {
    'schema': 'nested.yaml',
    'bad': 'nested_bad_data.yaml',
    'good': 'nested_good_data.yaml'
}

custom = {
    'schema': 'custom_types.yaml',
    'bad': 'custom_types_bad.yaml',
    'good': 'custom_types_good.yaml'
}

keywords = {
    'schema': 'keywords.yaml',
    'bad': 'keywords_bad.yaml',
    'good': 'keywords_good.yaml'
}

lists = {
    'schema': 'lists.yaml',
    'bad': 'lists_bad.yaml',
    'good': 'lists_good.yaml'
}

maps = {
    'schema': 'map.yaml',
    'bad': 'map_bad.yaml',
    'good': 'map_good.yaml'
}

anys = {
    'schema': 'any.yaml',
    'bad': 'any_bad.yaml',
    'good': 'any_good.yaml'
}

test_data = [types, nested, custom, keywords, lists, maps, anys]

for d in test_data:
    for key in d.keys():
        if key == 'schema':
            d[key] = yamale.make_schema(get_fixture(d[key]))
        else:
            d[key] = yamale.make_data(get_fixture(d[key]))


def test_tests():
    ''' Make sure the test runner is working.'''
    assert 1 + 1 == 2


def test_flat_make_schema():
    assert isinstance(types['schema']['string'], val.String)


def test_nested_schema():
    nested_schema = nested['schema']
    assert isinstance(nested_schema['string'], val.String)
    assert isinstance(nested_schema.dict['list'], (list, tuple))
    assert isinstance(nested_schema['list.0'], val.String)


def test_good():
    for data_map in test_data:
        yield good_gen, data_map


def good_gen(data_map):
    yamale.validate(data_map['schema'], data_map['good'])


def test_bad_validate():
    assert count_exception_lines(types['schema'], types['bad']) == 10


def test_bad_nested():
    assert count_exception_lines(nested['schema'], nested['bad']) == 4


def test_bad_custom():
    assert count_exception_lines(custom['schema'], custom['bad']) == 3


def test_bad_lists():
    assert count_exception_lines(lists['schema'], lists['bad']) == 6


def test_bad_maps():
    assert count_exception_lines(maps['schema'], maps['bad']) == 6


def test_bad_keywords():
    assert count_exception_lines(keywords['schema'], keywords['bad']) == 10


def test_bad_anys():
    assert count_exception_lines(anys['schema'], anys['bad']) == 7


def count_exception_lines(schema, data):
    try:
        yamale.validate(schema, data)
    except ValueError as exp:
        message = str(exp)
        count = len(message.split('\n'))
        return count
    raise Exception("Data valid")
