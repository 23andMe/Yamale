import os
from .. import command_line

dir_path = os.path.dirname(os.path.realpath(__file__))


def test_bad_yaml():
    try:
        command_line._router(
            'yamale/tests/command_line_fixtures/yamls/bad.yaml',
            'schema.yaml', 1)
    except ValueError as e:
        assert 'map.bad: \'12.5\' is not a str.' in str(e)
        return
    assert False


def test_good_yaml():
    command_line._router(
        'yamale/tests/command_line_fixtures/yamls/good.yaml',
        'schema.yaml', 1)


def test_good_relative_yaml():
    command_line._router(
        'yamale/tests/command_line_fixtures/yamls/good.yaml',
        '../schema_dir/external.yaml', 1)


def test_external_glob_schema():
    command_line._router(
        'yamale/tests/command_line_fixtures/yamls/good.yaml',
        os.path.join(dir_path, 'command_line_fixtures/schema_dir/ex*.yaml'), 1)


def test_external_schema():
    command_line._router(
        'yamale/tests/command_line_fixtures/yamls/good.yaml',
        os.path.join(dir_path, 'command_line_fixtures/schema_dir/external.yaml'), 1)


def test_bad_dir():
    try:
        command_line._router(
            'yamale/tests/command_line_fixtures/yamls',
            'schema.yaml', 4)
    except ValueError as e:
        assert 'map.bad: \'12.5\' is not a str.' in str(e)
        return
    assert False
