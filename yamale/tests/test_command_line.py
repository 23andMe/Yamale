import os

import pytest

from .. import command_line

dir_path = os.path.dirname(os.path.realpath(__file__))

parsers = ['pyyaml', 'PyYAML', 'ruamel']


@pytest.mark.parametrize('parser', parsers)
def test_bad_yaml(capsys, parser):
    assert command_line._router(
        'yamale/tests/command_line_fixtures/yamls/bad.yaml',
        'schema.yaml', 1, parser) == 1
    captured = capsys.readouterr()
    assert "map.bad: '12.5' is not a str." in captured.out


@pytest.mark.parametrize('parser', parsers)
def test_required_keys_yaml(capsys, parser):
    result = command_line._router(
        'yamale/tests/command_line_fixtures/yamls/required_keys_bad.yaml',
        'required_keys_schema.yaml', 1, parser)
    assert result == 1
    captured = capsys.readouterr()
    assert "map.key: Required field missing" in captured.out


@pytest.mark.parametrize('parser', parsers)
def test_good_yaml(parser):
    result = command_line._router(
        'yamale/tests/command_line_fixtures/yamls/good.yaml',
        'schema.yaml', 1, parser)
    assert result == 0


@pytest.mark.parametrize('parser', parsers)
def test_good_relative_yaml(parser):
    result = command_line._router(
        'yamale/tests/command_line_fixtures/yamls/good.yaml',
        '../schema_dir/external.yaml', 1, parser)
    assert result == 0


@pytest.mark.parametrize('parser', parsers)
def test_external_glob_schema(parser):
    result = command_line._router(
        'yamale/tests/command_line_fixtures/yamls/good.yaml',
        os.path.join(dir_path, 'command_line_fixtures/schema_dir/ex*.yaml'), 1, parser)
    assert result == 0


def test_empty_schema_file():
    with pytest.raises(ValueError, match='is an empty file!'):
        command_line._router(
            'yamale/tests/command_line_fixtures/empty_schema/data.yaml',
            'empty_schema.yaml' , 1, 'PyYAML')


def test_external_schema():
    command_line._router(
        'yamale/tests/command_line_fixtures/yamls/good.yaml',
        os.path.join(dir_path, 'command_line_fixtures/schema_dir/external.yaml'), 1, 'PyYAML')


def test_bad_dir(capsys):
    schema = 'yamale/tests/command_line_fixtures/schema.yaml'
    bad = 'yamale/tests/command_line_fixtures/yamls/bad.yaml'
    line = "Error validating data '%s' with '%s'" % (os.path.abspath(bad), os.path.abspath(schema))
    results = command_line._router(
        'yamale/tests/command_line_fixtures/yamls',
        'schema.yaml', 4, 'PyYAML')
    assert results == 1
    out, err = capsys.readouterr()
    assert 'Finding yaml files...' in out
    assert "Found 4 yaml files." in out
    assert "Validating..." in out
    assert line in out
    assert "map.bad: '12.5' is not a str." in out
    assert "map.bad: '12.5' is not a int." in out
    assert "map.not: '[]' is not a str." in out
    assert "map.not: '[]' is not a int." in out


def test_bad_strict(capsys):
    command_line._router(
        'yamale/tests/command_line_fixtures/yamls/required_keys_extra_element.yaml',
        'required_keys_schema.yaml',
        4, 'PyYAML', strict=True)
    captured = capsys.readouterr()
    assert "map.key2: Unexpected element" in captured.out


def test_bad_issue_54(capsys):
    command_line._router(
        'yamale/tests/fixtures/nested_issue_54.yaml',
        'nested.yaml',
        4, 'PyYAML', strict=True)
    captured = capsys.readouterr()
    assert 'string: Required field missing' in captured.out
    assert 'number: Required field missing' in captured.out
    assert 'integer: Required field missing' in captured.out
    assert 'boolean: Required field missing' in captured.out
    assert 'date: Required field missing' in captured.out
    assert 'datetime: Required field missing' in captured.out
    assert 'nest: Required field missing' in captured.out
    assert 'list: Required field missing' in captured.out
