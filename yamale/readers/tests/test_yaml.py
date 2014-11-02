from .. import yaml_reader
from yamale.tests import get_fixture


TYPES = get_fixture('types.yaml')
NESTED = get_fixture('nested.yaml')
KEYWORDS = get_fixture('keywords.yaml')


def test_parse():
    a = yaml_reader.parse_file(TYPES)[0]
    assert a['string'] == 'str()'


def test_types():
    t = yaml_reader.parse_file(TYPES)[0]
    assert t['string'] == 'str()'
    assert t['number'] == 'num()'
    assert t['boolean'] == 'bool()'
    assert t['integer'] == 'int()'


def test_keywords():
    t = yaml_reader.parse_file(KEYWORDS)[0]
    assert t['optional_min'] == 'int(min=1, required=False)'


def test_nested():
    t = yaml_reader.parse_file(NESTED)[0]
    assert t['list'][-1]['string'] == 'str()'
