import pytest
import yamale

from . import get_fixture
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
    'bad2': 'lists_bad2.yaml',
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

list_include = {
    'schema': 'list_include.yaml',
    'good': 'list_include_good.yaml'
}

issue_22 = {
    'schema': 'issue_22.yaml',
    'good': 'issue_22_good.yaml'
}

issue_50 = {
    'schema': 'issue_50.yaml',
    'good': 'issue_50_good.yaml'
}

regexes = {
    'schema': 'regex.yaml',
    'bad': 'regex_bad.yaml',
    'good': 'regex_good.yaml'
}

ips = {
    'schema': 'ip.yaml',
    'bad': 'ip_bad.yaml',
    'good': 'ip_good.yaml'
}

macs = {
    'schema': 'mac.yaml',
    'bad': 'mac_bad.yaml',
    'good': 'mac_good.yaml'
}

nested_map = {
    'schema': 'nested_map.yaml',
    'good': 'nested_map_good.yaml'
}

top_level_map = {
    'schema': 'top_level_map.yaml',
    'good': 'top_level_map_good.yaml'
}

include_validator = {
    'schema': 'include_validator.yaml',
    'good': 'include_validator_good.yaml',
    'bad': 'include_validator_bad.yaml'
}

strict_map = {
    'schema': 'strict_map.yaml',
    'good': 'strict_map_good.yaml',
    'bad': 'strict_map_bad.yaml'
}

mixed_strict_map = {
    'schema': 'mixed_strict_map.yaml',
    'good': 'mixed_strict_map_good.yaml',
    'bad': 'mixed_strict_map_bad.yaml'
}

strict_list = {
    'schema': 'strict_list.yaml',
    'good': 'strict_list_good.yaml',
    'bad': 'strict_list_bad.yaml'
}

nested_map2 = {
    'schema': 'nested_map2.yaml',
    'good': 'nested_map2_good.yaml',
    'bad': 'nested_map2_bad.yaml'
}

test_data = [
    types, nested, custom,
    keywords, lists, maps,
    anys, list_include, issue_22,
    issue_50, regexes, ips, macs,
    nested_map, top_level_map,
    include_validator, strict_map,
    mixed_strict_map, strict_list,
    nested_map2
]

for d in test_data:
    for key in d.keys():
        if key == 'schema':
            d[key] = yamale.make_schema(get_fixture(d[key]))
        else:
            d[key] = yamale.make_data(get_fixture(d[key]))


def test_tests():
    """ Make sure the test runner is working."""
    assert 1 + 1 == 2


def test_flat_make_schema():
    assert isinstance(types['schema']._schema['string'], val.String)


def test_nested_schema():
    nested_schema = nested['schema']._schema
    assert isinstance(nested_schema['string'], val.String)
    assert isinstance(nested_schema['list'], (list, tuple))
    assert isinstance(nested_schema['list'][0], val.String)


@pytest.mark.parametrize('data_map', test_data)
def test_good(data_map):
    yamale.validate(data_map['schema'], data_map['good'])


def test_bad_validate():
    assert count_exception_lines(types['schema'], types['bad']) == 11


def test_bad_nested():
    assert count_exception_lines(nested['schema'], nested['bad']) == 4


def test_bad_custom():
    assert count_exception_lines(custom['schema'], custom['bad']) == 3


def test_bad_lists():
    assert count_exception_lines(lists['schema'], lists['bad']) == 6


def test_bad2_lists():
    assert count_exception_lines(lists['schema'], lists['bad2']) == 3


def test_bad_maps():
    assert count_exception_lines(maps['schema'], maps['bad']) == 6


def test_bad_keywords():
    assert count_exception_lines(keywords['schema'], keywords['bad']) == 10


def test_bad_anys():
    assert count_exception_lines(anys['schema'], anys['bad']) == 7


def test_bad_regexes():
    assert count_exception_lines(regexes['schema'], regexes['bad']) == 9


def test_bad_include_validator():
    exp = ["key1: 'a_string' is not a int."]
    match_exception_lines(include_validator['schema'],
                          include_validator['bad'],
                          exp)


def test_bad_schema():
    with pytest.raises(SyntaxError) as excinfo:
        yamale.make_schema(get_fixture('bad_schema.yaml'))
    assert 'fixtures/bad_schema.yaml' in str(excinfo.value)


def test_list_is_not_a_map():
    exp = [": '[1, 2]' is not a map"]
    match_exception_lines(strict_map['schema'],
                          strict_list['good'],
                          exp)


def test_bad_strict_map():
    exp = ['extra: Unexpected element']
    match_exception_lines(strict_map['schema'],
                          strict_map['bad'],
                          exp,
                          strict=True)


def test_bad_strict_list():
    exp = ['2: Unexpected element']
    match_exception_lines(strict_list['schema'],
                          strict_list['bad'],
                          exp,
                          strict=True)


def test_bad_mixed_strict_map():
    exp = ['field3.extra: Unexpected element']
    match_exception_lines(mixed_strict_map['schema'],
                          mixed_strict_map['bad'],
                          exp)


def test_bad_nested_map2():
    exp = ['field1.field1_1: Required field missing']
    match_exception_lines(nested_map2['schema'],
                          nested_map2['bad'],
                          exp)


def match_exception_lines(schema, data, expected, strict=False):
    with pytest.raises(ValueError) as e:
        assert yamale.validate(schema, data, strict)

    message = str(e.value)
    # only match the actual error message and remove the leading \t
    got = set(s.lstrip() for s in message.split('\n') if s.startswith('\t'))
    expected = set(expected)
    assert got == expected


def count_exception_lines(schema, data, strict=False):
    try:
        yamale.validate(schema, data, strict)
    except ValueError as exp:
        message = str(exp)
        count = len(message.split('\n'))
        return count
    raise Exception("Data valid")
