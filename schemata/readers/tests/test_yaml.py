from .. import yaml
from schemata.tests import get_fixture


TYPES = get_fixture('types.yaml')
KEYWORDS = get_fixture('keywords.yaml')


def test_parse():
    a = yaml.parse_file(TYPES)
    assert a['string'] == 'str()'


def test_types():
    t = yaml.parse_file(TYPES)
    assert t['string'] == 'str()'
    assert t['number'] == 'num()'
    assert t['boolean'] == 'bool()'
    assert t['integer'] == 'int()'


def test_keywords():
    t = yaml.parse_file(KEYWORDS)
    assert t['optional_min'] == 'int(min=1, required=False)'
