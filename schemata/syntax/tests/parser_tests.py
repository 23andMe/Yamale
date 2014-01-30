from .. import parser as par
from schemata.validators import String


def test_eval():
    assert eval('String()') == String()


def test_types():
    assert par.parse('String()') == String()
    # assert isinstance(par.parse('str()'), val.String)
    # assert isinstance(par.parse('num()'), val.Number)
    # assert isinstance(par.parse('int()'), val.Integer)
    # assert isinstance(par.parse('bool()'), val.Boolean)


def test_required():
    pass
    # assert par.parse('str(required=True)').is_required
    # assert par.parse('str(required=False)').is_optional
