from .. import parser
from schemata import validators as val


def test_types():
    assert isinstance(parser.parse('str()'), val.String)
    assert isinstance(parser.parse('num()'), val.Number)
    assert isinstance(parser.parse('int()'), val.Integer)
    assert isinstance(parser.parse('bool()'), val.Boolean)

