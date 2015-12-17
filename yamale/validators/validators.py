import errno, os
from collections import Sequence, Mapping
from datetime import date, datetime
from .base import Validator
from . import constraints as con
from .. import util


class String(Validator):
    """String validator"""
    tag = 'str'
    constraints = [con.LengthMin, con.LengthMax, con.CharacterExclude]

    def _is_valid(self, value):
        return util.isstr(value)


class Pathname(Validator):
    '''
    Pathname validator, testing whether arbitrary objects are valid absolute or
    relative pathnames for the root filesystem of the current OS.

    Under:

    * POSIX-compatible OSes:
      * Valid pathnames are non-empty strings containing:
        * No null byte characters.
        * No `/`-delimited path component longer than 255 characters.
      * The root filesystem is the filesystem mounted to the root directory `/`.
    * Microsoft OSes:
      * Valid pathnames are non-empty strings satisfying `various constraints
        <https://msdn.microsoft.com/en-us/library/windows/desktop/aa365247%28v=vs.85%29.aspx>`_
        too numerous to document here.
      * The root filesystem is the filesystem to which this instance of Windows
        was installed, also given by the `%HOMEDRIVE%` environment variable.

    Parameters
    ----------
    _error_message : str
        OS-specific error message recorded by the most recent call to the
        `_is_valid()` method if any (e.g., `TypeError: embedded NUL character`)
        or `None` otherwise. If non-`None`, the `fail()` method subsequently
        embeds this message into a user-visible error message.
    '''
    tag = 'pathname'

    # Sadly, Python fails to provide the following magic numbers for us.
    ERROR_INVALID_NAME = 123
    '''
    Windows-specific error code indicating an invalid pathname.

    See Also
    ----------
    https://msdn.microsoft.com/en-us/library/windows/desktop/ms681382%28v=vs.85%29.aspx
        Official listing of all such codes.
    '''

    @staticmethod
    def get_root_dirname():
        '''
        Get the absolute path of the root directory for POSIX-compatible OSes or
        the value of the "%HOMEDRIVE%" environment variable (i.e., the drive to
        which Windows was installed) followed by a path separator for Windows.

        Returns
        ----------
        str
            Desired path, guaranteed to be terminated by a path separator.
        '''
        if util.is_os_windows_vanilla():
            return os.environ.get('HOMEDRIVE', 'C:') + os.path.sep
        else:
            return os.path.sep


    def _is_valid(self, value):
        # Reset the error message recorded by this call (if any).
        self._error_message = None

        # If this value is either a non-string or the empty string, this value
        # cannot by definition be a valid pathname.
        if not (util.isstr(value) and value):
            return False

        # The only cross-platform and -filesystem portable means of validating
        # pathnames is to parse exceptions raised by the kernel-dependent
        # os.stat() or os.lstat() functions for metadata indicating invalid
        # pathname syntax. All other approaches (e.g., regex string matching)
        # fail for common edge cases. See also:
        #     https://stackoverflow.com/a/34102855/2809027
        try:
            # Strip this pathname's Windows drive specifier (e.g., "C:\") if
            # any. Since Windows prohibits path components from containing ":"
            # characters, failing to strip this ":"-suffixed prefix would
            # erroneously invalidate all valid absolute Windows pathnames.
            _, value = os.path.splitdrive(value)

            # Absolute path of a directory guaranteed to exist.
            #
            # To avoid race conditions with external processes concurrently
            # modifying the filesystem, the passed pathname cannot be tested as
            # is. Only path components split from this pathname are safely
            # testable. Why? Because os.stat() and os.lstat() raise
            # "FileNotFoundError" exceptions when passed pathnames residing in
            # non-existing directories regardless of whether these pathnames are
            # invalid or not. Directory existence takes precedence over pathname
            # invalidity. Hence, the only means of testing whether pathnames are
            # invalid or not is to:
            #
            # 1. Split the passed pathname into path components (e.g.,
            #    "/foo/bar" into "['', 'foo', 'bar']").
            # 2. For each path component:
            #    1. Join the pathname of a directory guaranteed to exist and the
            #       current path component into a new pathname (e.g., "/bar").
            #    2. Pass that pathname to os.stat() or os.lstat(). If that
            #       pathname and hence current path component is invalid, this
            #       call is guaranteed to raise an exception exposing the type
            #       of invalidity rather than a generic "FileNotFoundError"
            #       exception. Why? Because that pathname resides in an
            #       existing directory. Circular logic is circular.
            #
            # Is there a directory guaranteed to exist? There is, but typically
            # only one: the root directory for the current filesystem. Passing
            # pathnames residing in any other directories to os.stat() or
            # os.lstat() invites mind-flaying race conditions, even for
            # directories previously tested to exist. Why? Because external
            # processes cannot be prevented from concurrently removing those
            # directories after those tests have been performed but before those
            # pathnames are passed to os.stat() or os.lstat().
            #
            # Did we mention this should be shipped with Python already?
            root_dirname = self.get_root_dirname()
            assert os.path.isdir(root_dirname)   # ...Murphy and her dumb Law

            # Test whether each path component split from this pathname is valid
            # or not. Most path components will *NOT* actually physically exist.
            for pathname_part in value.split(os.path.sep):
                try:
                    os.lstat(root_dirname + pathname_part)
                # If an OS-specific exception is raised, its error code
                # indicates whether this pathname is valid or not. Unless this
                # is the case, this exception implies an ignorable kernel or
                # filesystem complaint (e.g., path not found or inaccessible).
                #
                # Only the following exceptions indicate invalid pathnames:
                #
                # * Instances of the Windows-specific "WindowsError" class
                #   defining the "winerror" attribute whose value is
                #   "ERROR_INVALID_NAME". Under Windows, "winerror" is more
                #   fine-grained and hence useful than the generic "errno"
                #   attribute. When a too-long pathname is passed, for example,
                #   "errno" is "ENOENT" (i.e., no such file or directory) rather
                #   than "ENAMETOOLONG" (i.e., file name too long).
                # * Instances of the cross-platform "OSError" class defining the
                #   generic "errno" attribute whose value is either:
                #   * Under most POSIX-compatible OSes, "ENAMETOOLONG".
                #   * Under some edge-case OSes (e.g., SunOS, *BSD), "ERANGE".
                except OSError as exc:
                    if hasattr(exc, 'winerror'):
                        if exc.winerror == self.ERROR_INVALID_NAME:
                            self._error_message = exc.strerror
                            return False
                    elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                        self._error_message = exc.strerror
                        return False
        # If a "TypeError" exception was raised, it almost certainly has the
        # error message "embedded NUL character" indicating an invalid pathname.
        except TypeError as exc:
            self._error_message = str(exc)
            return False
        # If no exception was raised, all path components and hence this
        # pathname itself are valid. (Praise be to the curmudgeonly python.)
        else:
            return True
        # If any other exception was raised, this is an unrelated fatal issue
        # (e.g., a bug). Permit this exception to unwind the call stack.


    def fail(self, value):
        error_prefix = '%r is not a %s' % (value, self.get_name())

        # If the prior _is_valid() call recorded an error message, embed that.
        if self._error_message:
            error_prefix += ' (%s)' % self._error_message

        return error_prefix + '.'


class Path(Pathname):
    '''
    Path validator, testing whether arbitrary objects are valid pathnames of
    either existing files or directories to which the current user has
    `os.stat()` permissions _before_ following symbolic links.

    Relative paths are relative to the current working directory (CWD) rather
    than the parent directory of the current YAML data or schema files.

    For POSIX compliance, this validator always returns `True` when passed
    **dangling symbolic links** (i.e., existing symbolic links whose targets do
    _not_ currently exist) on POSIX-compatible OSes.
    '''
    tag = 'path'

    def _is_valid(self, value):
        # Test whether this value is a valid pathname first, as the subsequent
        # call raises exceptions for invalid pathnames.
        try:
            return super(Path, self)._is_valid(value) and os.path.lexists(value)
        # Report failure on non-fatal filesystem complaints (e.g., connection
        # timeouts, permissions issues) implying this path to be inaccessible.
        # All other exceptions are unrelated issues to be caught by the caller.
        except OSError as exc:
            self._error_message = exc.strerror
            return False


class Directory(Path):
    '''
    Directory validator, testing whether arbitrary objects are valid pathnames
    of existing directories to which the current user has `os.stat()`
    permissions _after_ following symbolic links.
    '''
    tag = 'dir'

    def _is_valid(self, value):
        # Test whether this value is a valid pathname first, as above.
        try:
            return super(Path, self)._is_valid(value) and os.path.isdir(value)
        # Report failure on non-fatal filesystem complaints (e.g., connection
        # timeouts, permissions issues) implying this path to be inaccessible.
        # All other exceptions are unrelated issues to be caught by the caller.
        except OSError as exc:
            self._error_message = exc.strerror
            return False


class File(Path):
    '''
    File validator, testing whether arbitrary objects are valid pathnames of
    existing **regular files** (i.e., paths that are _not_ special, which
    includes directories, dangling symbolic links, device nodes, named pipes,
    and sockets) to which the current user has `os.stat()` permissions _after_
    following symbolic links.
    '''
    tag = 'file'

    def _is_valid(self, value):
        # Test whether this value is a valid pathname first, as above.
        try:
            return super(Path, self)._is_valid(value) and os.path.isfile(value)
        # Report failure on non-fatal filesystem complaints (e.g., connection
        # timeouts, permissions issues) implying this path to be inaccessible.
        # All other exceptions are unrelated issues to be caught by the caller.
        except OSError as exc:
            self._error_message = exc.strerror
            return False


class Number(Validator):
    """Number/float validator"""
    value_type = float
    tag = 'num'
    constraints = [con.Min, con.Max]

    def _is_valid(self, value):
        return isinstance(value, (int, float))


class Integer(Validator):
    """Integer validator"""
    value_type = int
    tag = 'int'
    constraints = [con.Min, con.Max]

    def _is_valid(self, value):
        return isinstance(value, int)


class Boolean(Validator):
    """Boolean validator"""
    tag = 'bool'

    def _is_valid(self, value):
        return isinstance(value, bool)


class Enum(Validator):
    """Enum validator"""
    tag = 'enum'

    def __init__(self, *args, **kwargs):
        super(Enum, self).__init__(*args, **kwargs)
        self.enums = args

    def _is_valid(self, value):
        return value in self.enums

    def fail(self, value):
        return '\'%s\' not in %s' % (value, self.enums)


class Day(Validator):
    """Day validator. Format: YYYY-MM-DD"""
    value_type = date
    tag = 'day'
    constraints = [con.Min, con.Max]

    def _is_valid(self, value):
        return isinstance(value, date)


class Timestamp(Validator):
    """Timestamp validator. Format: YYYY-MM-DD HH:MM:SS"""
    value_type = datetime
    tag = 'timestamp'
    constraints = [con.Min, con.Max]

    def _is_valid(self, value):
        return isinstance(value, datetime)


class Map(Validator):
    """Map and dict validator"""
    tag = 'map'

    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        self.validators = [val for val in args if isinstance(val, Validator)]

    def _is_valid(self, value):
        return isinstance(value, Mapping)


class List(Validator):
    """List validator"""
    tag = 'list'
    constraints = [con.LengthMin, con.LengthMax]

    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
        self.validators = [val for val in args if isinstance(val, Validator)]

    def _is_valid(self, value):
        return isinstance(value, Sequence) and not util.isstr(value)


class Include(Validator):
    """Include validator"""
    tag = 'include'

    def __init__(self, *args, **kwargs):
        self.include_name = args[0]
        super(Include, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        return isinstance(value, (Mapping, Sequence)) and not util.isstr(value)

    def get_name(self):
        return self.include_name


class Any(Validator):
    """Any of several types validator"""
    tag = 'any'

    def __init__(self, *args, **kwargs):
        self.validators = [val for val in args if isinstance(val, Validator)]
        super(Any, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        return True


class Null(Validator):
    """Validates null"""
    value_type = None
    tag = 'null'

    def _is_valid(self, value):
        return value is None


DefaultValidators = {}

for v in util.get_subclasses(Validator):
    # Allow validator nodes to contain either tags or actual name
    DefaultValidators[v.tag] = v
    DefaultValidators[v.__name__] = v
