from nose.tools import raises
from ... import readers


@raises(ValueError)
def test_reader_error():
    readers.parse_file('wat', reader='notareader')
