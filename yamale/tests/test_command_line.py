import os

import pytest

from .. import command_line

dir_path = os.path.dirname(os.path.realpath(__file__))

parsers = ['pyyaml', 'PyYAML', 'ruamel']


@pytest.mark.parametrize('parser', parsers)
def test_bad_yaml(capsys, parser):
    try:
        command_line._router(
            'yamale/tests/command_line_fixtures/yamls/bad.yaml',
            'schema.yaml', 1, parser)
    except ValueError as e:
        assert 'Validation failed!' in str(e)
        captured = capsys.readouterr()
        assert "map.bad: '12.5' is not a str." in captured.out
        return
    assert False


@pytest.mark.parametrize('parser', parsers)
def test_required_keys_yaml(capsys, parser):
    try:
        command_line._router(
            'yamale/tests/command_line_fixtures/yamls/required_keys_bad.yaml',
            'required_keys_schema.yaml', 1, parser)
    except ValueError as e:
        assert 'Validation failed!' in str(e)
        captured = capsys.readouterr()
        assert "map.key: Required field missing" in captured.out
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


def test_bad_strict(capsys):
    try:
        command_line._router(
            'yamale/tests/command_line_fixtures/yamls/required_keys_extra_element.yaml',
            'required_keys_schema.yaml',
            4, 'PyYAML', strict=True)
    except ValueError as e:
        assert 'Validation failed!' in str(e)
        captured = capsys.readouterr()
        assert "map.key2: Unexpected element" in captured.out
        return
    assert False
