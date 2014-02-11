from nose.tools import raises

from .. import parser as par
from ...validators.validators import *


def test_eval():
    assert eval('String()') == String()


def test_types():
    assert par.parse('String()') == String()
    assert par.parse('str()') == String()
    assert par.parse('num()') == Number()
    assert par.parse('int()') == Integer()
    assert par.parse('bool()') == Boolean()
    assert par.parse('list(str())') == List(String())


def test_required():
    assert par.parse('str(required=True)').is_required
    assert par.parse('str(required=False)').is_optional


@raises(SyntaxError)
def test_syntax_error():
    par.parse('eval()')
