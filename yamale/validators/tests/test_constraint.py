import datetime
from ... import validators as val


def test_default():
    v = val.Number(default=0)
    assert v.is_valid(1)
    assert v.is_valid(1.3425235)
    assert not v.is_valid('str')


def test_length_min():
    v = val.String(min=2)
    assert v.is_valid('abcd')
    assert v.is_valid('ab')
    assert not v.is_valid('a')


def test_length_max():
    v = val.String(max=3)
    assert v.is_valid('abc')
    assert v.is_valid('ab')
    assert not v.is_valid('abcd')


def test_number_max():
    v = val.Number(min=.5)
    assert v.is_valid(4)
    assert v.is_valid(.5)
    assert not v.is_valid(.1)


def test_number_min():
    v = val.Integer(max=10)
    assert v.is_valid(4)
    assert v.is_valid(10)
    assert not v.is_valid(11)


def test_timestamp_min():
    v = val.Timestamp(min=datetime.datetime(2010, 1, 1))
    assert v.is_valid(datetime.datetime(2010, 1, 1))
    assert v.is_valid(datetime.datetime(2011, 2, 2))
    assert not v.is_valid(datetime.datetime(2009, 12, 31))


def test_timestamp_max():
    v = val.Timestamp(max=datetime.datetime(2010, 1, 1))
    assert v.is_valid(datetime.datetime(2010, 1, 1))
    assert v.is_valid(datetime.datetime(2009, 2, 2))
    assert not v.is_valid(datetime.datetime(2010, 2, 2))


def test_day_min():
    v = val.Day(min=datetime.date(2010, 1, 1))
    assert v.is_valid(datetime.date(2010, 1, 1))
    assert v.is_valid(datetime.date(2011, 2, 2))
    assert not v.is_valid(datetime.date(2009, 12, 31))


def test_day_max():
    v = val.Day(max=datetime.date(2010, 1, 1))
    assert v.is_valid(datetime.date(2010, 1, 1))
    assert v.is_valid(datetime.date(2009, 2, 2))
    assert not v.is_valid(datetime.date(2010, 2, 2))


def test_char_exclude():
    v = val.String(exclude='abcd')
    assert v.is_valid('efg')
    assert not v.is_valid('abc')
    assert not v.is_valid('c')
