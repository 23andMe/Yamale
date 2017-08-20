import pytest
from pytest import raises
from .. import parse_file

parsers = ['pyyaml', 'PyYAML', 'ruamel']


@pytest.mark.parametrize('parser', parsers)
def test_reader_error(parser):
    with raises(IOError):
        parse_file('wat', parser)
