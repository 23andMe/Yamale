from datetime import date, datetime
from yamale import validators as val


def test_validator_defaults():
    """
    Unit test the dictionary of default validators.
    """
    assert val.DefaultValidators[val.String.tag] is val.String
    assert val.DefaultValidators[val.Any.__name__] is val.Any


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


def test_regex():
    v = val.Regex(r'^(abc)\1?de$', name='test regex')
    assert v.is_valid('abcabcde')
    assert not v.is_valid('abcabcabcde')
    assert not v.is_valid('\12')
    assert v.fail('woopz') == '\'woopz\' is not a test regex.'

    v = val.Regex('[a-z0-9]{3,}s\s$', ignore_case=True)
    assert v.is_valid('b33S\v')
    assert v.is_valid('B33s\t')
    assert not v.is_valid(' b33s ')
    assert not v.is_valid('b33s  ')
    assert v.fail('fdsa') == '\'fdsa\' is not a regex match.'

    v = val.Regex('A.+\d$', ignore_case=False, multiline=True)
    assert v.is_valid('A_-3\n\n')
    assert not v.is_valid('a!!!!!5\n\n')

    v = val.Regex('.*^Ye.*s\.', ignore_case=True, multiline=True, dotall=True)
    assert v.is_valid('YEeeEEEEeeeeS.')
    assert v.is_valid('What?\nYes!\nBEES.\nOK.')
    assert not v.is_valid('YES-TA-TOES?')
    assert not v.is_valid('\n\nYaes.')


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
