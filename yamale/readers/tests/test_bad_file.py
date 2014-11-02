from nose.tools import raises
from .. import parse_file


@raises(IOError)
def test_reader_error():
    parse_file('wat')
