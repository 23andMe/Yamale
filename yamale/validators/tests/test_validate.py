import os, tempfile
from datetime import date, datetime
from ... import validators as val
from ... import util


def test_validator_defaults():
    '''
    Unit test the dictionary of default validators.
    '''

    # Ensure direct "Validator" subclasses are available by default.
    assert val.DefaultValidators[val.String.tag] is val.String
    assert val.DefaultValidators[val.Any.__name__] is val.Any

    # Ensure transitive "Validator" subclasses are also available by default.
    assert val.DefaultValidators[val.Path.tag] is val.Path
    assert val.DefaultValidators[val.File.__name__] is val.File


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


def test_validator_pathname():
    '''
    Unit test the `Pathname` validator.
    '''

    v = val.Pathname()

    # Absolute path of a directory guaranteed to exist. See Pathname._is_valid().
    root_dirname = val.Pathname.get_root_dirname()

    # Directory substantially unlikely to exist but otherwise valid for all
    # known filesystems. (The ghost of MS-DOS haunts us still.)
    missing_dirname = os.path.join(
        root_dirname,
        '_nO_sUch.dIr',
        '_nOsIrEE.bOb')

    # Path component exceeding the maximum length for all known filesystems and
    # hence invalid. See the "Maximum filename length" table column at:
    #     https://en.wikipedia.org/wiki/Comparison_of_file_systems
    long_basename = 'a' * 16000

    # The above directory and the current directory are valid pathnames.
    assert v.is_valid(root_dirname)
    assert v.is_valid(os.getcwd())

    # Non-strings and the empty string are invalid pathnames.
    assert not v.is_valid(1)
    assert not v.is_valid(True)
    assert not v.is_valid('')

    # If the current OS is Windows, a colon is an invalid pathname. See also:
    #     https://msdn.microsoft.com/en-us/library/windows/desktop/aa365247(v=vs.85).aspx
    #
    # To exercise edge cases both here and below, invalid path components in
    # non-existing directories are verified to be invalid as well.
    if util.is_os_windows_vanilla():
        assert not v.is_valid(':')
        assert not v.is_valid(os.path.join(missing_dirname, ':'))
    # Else, the current OS is assume to be POSIX-compatible, in which case the
    # null byte is an invalid pathname.
    #
    # Curiously, Windows permits a pathname to contain arbitrarily many null
    # bytes, the first of which silently terminates that pathname. Although this
    # implies a pathname consisting only of a null byte to be semantically
    # equivalent to the empty string and hence invalid, Windows erroneously
    # raises the generic "ERROR_PATH_NOT_FOUND" error rather than the expected
    # "ERROR_INVALID_NAME" error on statting this pathname. (Anger... rising.)
    else:
        assert not v.is_valid('\x00')
        assert not v.is_valid(os.path.join(missing_dirname, '\x00'))

    # If the current OS is not Windows, long path components are invalid
    # pathnames. Although this is technically the case under Windows as well,
    # Windows erroneously raises the generic "ERROR_PATH_NOT_FOUND" error rather
    # than the expected "ERROR_INVALID_NAME" error on statting pathnames
    # containing long path components. While this could be resolved for the
    # specific cases of the NTFS and FAT-derived filesystems (e.g., by testing
    # path component string lengths), there's no guarantee that all future
    # Microsoft filesystems will impose the same constraint and hence no
    # reliable means of validating this constraint. So we don't.
    if not util.is_os_windows_vanilla():
        assert not v.is_valid(long_basename)
        assert not v.is_valid(os.path.join(missing_dirname, long_basename))


def test_validator_path():
    '''
    Unit test the `Path` validator.
    '''

    # Ensure the `Path` validator validates both directory and file existence.
    v = val.Path()
    _validate_directory(v)
    _validate_file(v)


def test_validator_directory():
    '''
    Unit test the `Directory` validator.
    '''

    _validate_directory(val.Directory())


def test_validator_file():
    '''
    Unit test the `File` validator.
    '''

    _validate_file(val.File())


def _validate_directory(v):
    '''
    Test the passed validator for use in validating directory existence.
    '''

    # A temporary named directory always exists during its context, ignoring
    # unlikely edge-case race conditions in which this directory is removed.
    # Ideally, this would use the "tempfile.TemporaryDirectory" class to do so;
    # since that class is Python 3-specific, mkdtemp() is used instead.
    try:
        temp_dirname = tempfile.mkdtemp()
        assert v.is_valid(temp_dirname)
    # Remove this directory. Ignoring edge-case race conditions, this directory
    # should both still exist and be empty.
    finally:
        os.rmdir(temp_dirname)

    # The same directory never exists immediately after its context, ignoring
    # unlikely edge-case race conditions in which this directory is recreated.
    assert not v.is_valid(temp_dirname)


def _validate_file(v):
    '''
    Test the passed validator for use in validating file existence.
    '''

    # A temporary named file always exists during its context. (See above.)
    with tempfile.NamedTemporaryFile() as temp_filename:
        assert v.is_valid(temp_filename.name)

    # The same file never exists immediately after its context. (See above.)
    assert not v.is_valid(temp_filename.name)


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
