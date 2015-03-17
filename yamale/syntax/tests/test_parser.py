from pytest import raises

from .. import parser as par
from ...validators.validators import (Validator, String, Number,
                                      Integer, Boolean, List, Day, Timestamp)


def test_eval():
    assert eval('String()') == String()


def test_types():
    assert par.parse('String()') == String()
    assert par.parse('str()') == String()
    assert par.parse('num()') == Number()
    assert par.parse('int()') == Integer()
    assert par.parse('day()') == Day()
    assert par.parse('timestamp()') == Timestamp()
    assert par.parse('bool()') == Boolean()
    assert par.parse('list(str())') == List(String())


def test_custom_type():

    class my_validator(Validator):
        pass

    assert par.parse('custom()', {'custom': my_validator}) == my_validator()


def test_required():
    assert par.parse('str(required=True)').is_required
    assert par.parse('str(required=False)').is_optional


def test_syntax_error():
    with raises(SyntaxError):
        par.parse('eval()')
