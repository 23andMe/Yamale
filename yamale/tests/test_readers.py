import pytest
import datetime

import yaml 
from yaml import SafeLoader

from ruamel.yaml import YAML 

from .. import util
from .. import readers 


DATE_LIST = ['2010-01-01', '2001-1-1', '2001-01-01T12:00:00', '2001-1-1t12:00:00', '2001-1-1 12:00:00', '2001-1-1 12:00', 'thisisnotadate']

def test_converter(): 
    # Test that util function converts datetime strings properly
    assert isinstance(util.parse_default_date('2001-01-01'), datetime.date)
    assert isinstance(util.parse_default_date('2001-01-01T12:00:00'), datetime.datetime)
    assert isinstance(util.parse_default_date('2001-1-1t12:00:00'), datetime.datetime)
    assert isinstance(util.parse_default_date('2001-1-1 12:00:00'), datetime.datetime)

    assert isinstance(util.parse_default_date('01/01/2010'), str)
    assert isinstance(util.parse_default_date('2010-1-1'), str)
    assert isinstance(util.parse_default_date('2001-1-1 12:00'), str)
    assert isinstance(util.parse_default_date('thisisnotadate'), str)


def test_pyyaml_base_case(): 
    # Test that util function converts dates the same as pyyaml Safeloader 
    for i in DATE_LIST: 
        date_one = util.parse_default_date(i)
        date_two = list(yaml.load_all('date: %s' % i, Loader=SafeLoader))[0]['date']
        assert type(date_one) == type(date_two)

def test_ruamel_base_case(): 
    # Test that util function converts dates to the same as ruamel base loader
    r_yaml = YAML(typ='safe')
    
    for i in DATE_LIST: 
        date_one = util.parse_default_date(i)
        date_two = list(r_yaml.load_all(i))[0]
        assert type(date_one) == type(date_two)


def get_date(yaml_string, parser): 
    data = list(readers.parse_yaml(parser=parser, content=yaml_string))
    return data[0]['date']


def test_pyyaml_NoDatesSafeLoader(): 
    # Test that NoDatesSafeLoader loads all date-like strings as strings
    for i in DATE_LIST: 
        date = get_date('date: %s' % i, 'pyyaml')
        assert isinstance(date, str)


def test_ruamel_loader():
    # Test that ruamel loader loads datetime-like strings as strings
    for i in DATE_LIST: 
        date = get_date('date: %s' % i, 'ruamel')
        assert isinstance(date, str)
