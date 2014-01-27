from .. import yaml
import os

script_dir = os.path.dirname(__file__)
SIMPLE = os.path.join(script_dir, 'fixtures/simple.yaml')


def test_parse():
    a = yaml.parse_file(SIMPLE)
    print a
    assert a['int'] == 42
