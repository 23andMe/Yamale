from pytest import raises
from .. import parse_file


def test_reader_error():
    with raises(IOError):
        parse_file('wat')
