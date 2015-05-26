from datetime import date, datetime
from ... import validators as val


def test_equality():
    assert val.String() == val.String()
    assert val.String(hello='wat') == val.String(hello='wat')
    assert val.String(hello='wat') != val.String(hello='nope')
    assert val.Boolean('yep') != val.Boolean('nope')


def test_integer():
    v = val.Integer()
    assert v.is_valid(1)
    assert not v.is_valid('1')
    assert not v.is_valid(1.34)


def test_string():
    v = val.String()
    assert v.is_valid('1')
    assert not v.is_valid(1)


def test_number():
    v = val.Number()
    assert v.is_valid(1)
    assert v.is_valid(1.3425235)
    assert not v.is_valid('str')


def test_boolean():
    v = val.Boolean()
    assert v.is_valid(True)
    assert v.is_valid(False)
    assert not v.is_valid('')
    assert not v.is_valid(0)


def test_date():
    v = val.Day()
    assert v.is_valid(date(2015, 1, 1))
    assert v.is_valid(datetime(2015, 1, 1, 1))
    assert not v.is_valid('')
    assert not v.is_valid(0)


def test_datetime():
    v = val.Timestamp()
    assert v.is_valid(datetime(2015, 1, 1, 1))
    assert not v.is_valid(date(2015, 1, 1))
    assert not v.is_valid('')
    assert not v.is_valid(0)


def test_list():
    v = val.List()
    assert v.is_valid([])
    assert v.is_valid(())
    assert not v.is_valid('')
    assert not v.is_valid(0)


def test_null():
    v = val.Null()
    assert v.is_valid(None)
    assert not v.is_valid('None')
    assert not v.is_valid(0)
    assert not v.is_valid(float('nan'))
    assert not v.is_valid({})
