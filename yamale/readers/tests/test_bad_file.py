import pytest
from pytest import raises
from .. import parse_yaml

parsers = ["pyyaml", "PyYAML", "ruamel"]


@pytest.mark.parametrize("parser", parsers)
def test_reader_error(parser):
    with raises(IOError):
        parse_yaml("wat", parser)


@pytest.mark.parametrize("parser", parsers)
def test_malformed_yaml_raises_value_error(parser):
    # Malformed YAML should surface as a clean ValueError instead of leaking
    # the underlying parser's ScannerError/YAMLError as a stack trace (#282).
    with raises(ValueError):
        parse_yaml(content='key: "unclosed', parser=parser)
