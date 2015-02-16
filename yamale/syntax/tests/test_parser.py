from pytest import raises

from .. import parser as par
from ...validators.validators import (Validator, String, Number, Integer, Boolean, List)
from ...validators import DefaultValidators

def test_eval():
    assert eval('String()') == String()


def test_types():
    assert par.parse('String()', DefaultValidators) == String()
    assert par.parse('str()', DefaultValidators) == String()
    assert par.parse('num()', DefaultValidators) == Number()
    assert par.parse('int()', DefaultValidators) == Integer()
    assert par.parse('bool()', DefaultValidators) == Boolean()
    assert par.parse('list(str())', DefaultValidators) == List(String())


def test_custom_type():

    class my_validator(Validator):
        pass

    assert par.parse('custom()', {'custom': my_validator}) == my_validator()


def test_required():
    assert par.parse('str(required=True)', DefaultValidators).is_required
    assert par.parse('str(required=False)', DefaultValidators).is_optional


def test_syntax_error():
    with raises(SyntaxError):
        par.parse('eval()', DefaultValidators)
