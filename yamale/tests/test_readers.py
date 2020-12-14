import pytest
from .. import util
from .. import readers

def get_date(yaml_string, parser): 
    data = list(readers.parse_file(yaml_string, parser=parser))
    return data[0]['date']

def test_pyyaml_loader(): 
    # Test that NoDateSafeLoader loads datetimes as strings
    assert isinstance(get_date('date: 2010-01-01', 'PyYAML'), str)

def test_pyyaml_converter(): 
    # Test that util function converts datetimes the same 
    # as the standard PyYAML datetime constructor


def test_ruamel_loader():
    # Test that ruamel loader loads datetimes as strings
    assert isinstance(get_date('date: 2010-01-01', 'ruamel'), str)

def test_ruamel_converter(): 
    # Test that util function converts datetimes the same 
    # as the standard ruamel datetime constructor

