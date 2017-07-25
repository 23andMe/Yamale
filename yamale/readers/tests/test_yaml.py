import pytest
from .. import yaml_reader
from yamale.tests import get_fixture

parsers = ['pyyaml', 'PyYAML', 'ruamel']
TYPES = get_fixture('types.yaml')
NESTED = get_fixture('nested.yaml')
KEYWORDS = get_fixture('keywords.yaml')


@pytest.mark.parametrize('parser', parsers)
def test_parse(parser):
    a = yaml_reader.parse_file(TYPES, parser)[0]
    assert a['string'] == 'str()'


@pytest.mark.parametrize('parser', parsers)
def test_types(parser):
    t = yaml_reader.parse_file(TYPES, parser)[0]
    assert t['string'] == 'str()'
    assert t['number'] == 'num()'
    assert t['boolean'] == 'bool()'
    assert t['integer'] == 'int()'


@pytest.mark.parametrize('parser', parsers)
def test_keywords(parser):
    t = yaml_reader.parse_file(KEYWORDS, parser)[0]
    assert t['optional_min'] == 'int(min=1, required=False)'


@pytest.mark.parametrize('parser', parsers)
def test_nested(parser):
    t = yaml_reader.parse_file(NESTED, parser)[0]
    assert t['list'][-1]['string'] == 'str()'
