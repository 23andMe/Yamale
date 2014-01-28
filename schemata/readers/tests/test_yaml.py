from .. import yaml
from schemata.validators.validators import String, Number, Boolean, Integer
from schemata.tests import get_fixture


TYPES = get_fixture('types.yaml')
KEYWORDS = get_fixture('keywords.yaml')


def test_parse():
    a = yaml.parse_file(TYPES)
    assert a['string'] == 'str()'


def test_types():
    t = yaml.parse_file(TYPES)
    assert isinstance(t['string'], String)
    assert isinstance(t['number'], Number)
    assert isinstance(t['boolean'], Boolean)
    assert isinstance(t['integer'], Integer)


def test_keywords():
    t = yaml.parse_file(KEYWORDS)
    assert t['optional'].is_optional
    assert t['min'].is_required
    assert '?str' not in t['optional'].args
    assert t['optional_min'].min == 1
    for arg in t['optional_min'].args:
        assert '=' not in arg
    assert t['default'].default is True
    assert t['max'].max == 100
