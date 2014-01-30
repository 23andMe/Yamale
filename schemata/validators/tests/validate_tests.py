from ... import validators as val


def test_integer():
    v = val.Integer()
    assert v.is_valid(1)
    assert not v.is_valid('1')

    v = val.String()
    assert v.is_valid('1')
    assert not v.is_valid(1)


def test_equality():
    assert val.String() == val.String()
    assert val.String(hello='wat') == val.String(hello='wat')
    assert val.String(hello='wat') != val.String(hello='nope')
    assert val.Boolean('yep') != val.Boolean('nope')
