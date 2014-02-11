from ... import validators as val


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


def test_char_exclude():
    v = val.String(exclude='abcd')
    assert v.is_valid('efg')
    assert not v.is_valid('abc')
    assert not v.is_valid('c')
