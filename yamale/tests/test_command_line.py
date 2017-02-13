import pytest
from .. import command_line


def test_bad_yaml():
    with pytest.raises(ValueError):
        command_line._router(
            'yamale/tests/command_line_fixtures/yamls/bad.yaml',
            'schema.yaml', 1)


def test_good_yaml():
    command_line._router(
        'yamale/tests/command_line_fixtures/yamls/good.yaml',
        'schema.yaml', 1)


def test_bad_dir():
    with pytest.raises(ValueError):
        command_line._router(
            'yamale/tests/command_line_fixtures',
            'schema.yaml', 4)
