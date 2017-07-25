import os

import pytest

from .. import command_line

dir_path = os.path.dirname(os.path.realpath(__file__))

parsers = ['pyyaml', 'PyYAML', 'ruamel']


@pytest.mark.parametrize('parser', parsers)
def test_bad_yaml(parser):
    try:
        command_line._router(
            'yamale/tests/command_line_fixtures/yamls/bad.yaml',
            'schema.yaml', 1, parser)
    except ValueError as e:
        assert 'Validation failed!' in str(e)
        return
    assert False


@pytest.mark.parametrize('parser', parsers)
def test_good_yaml(parser):
    command_line._router(
        'yamale/tests/command_line_fixtures/yamls/good.yaml',
        'schema.yaml', 1, parser)


@pytest.mark.parametrize('parser', parsers)
def test_good_relative_yaml(parser):
    command_line._router(
        'yamale/tests/command_line_fixtures/yamls/good.yaml',
        '../schema_dir/external.yaml', 1, parser)


@pytest.mark.parametrize('parser', parsers)
def test_external_glob_schema(parser):
    command_line._router(
        'yamale/tests/command_line_fixtures/yamls/good.yaml',
        os.path.join(dir_path, 'command_line_fixtures/schema_dir/ex*.yaml'), 1, parser)


def test_external_schema():
    command_line._router(
        'yamale/tests/command_line_fixtures/yamls/good.yaml',
        os.path.join(dir_path, 'command_line_fixtures/schema_dir/external.yaml'), 1, 'PyYAML')


def test_bad_dir():
    try:
        command_line._router(
            'yamale/tests/command_line_fixtures/yamls',
            'schema.yaml', 4, 'PyYAML')
    except ValueError as e:
        assert 'Validation failed!' in str(e)
        return
    assert False
