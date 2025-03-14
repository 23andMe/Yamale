from __future__ import absolute_import
import re
import datetime
import ipaddress

from yamale.util import to_unicode
from .base import Validator
from .. import util


class Constraint(object):
    keywords = {}  # Keywords and types accepted by this constraint
    is_active = False
    pre_check = False
    universal = False

    def __init__(self, value_type, kwargs):
        self._parseKwargs(kwargs)

    def _parseKwargs(self, kwargs):
        for kwarg, kwtype in self.keywords.items():
            value = self.get_kwarg(kwargs, kwarg, kwtype)
            setattr(self, kwarg, value)

    def get_kwarg(self, kwargs, key, kwtype):
        try:
            value = kwargs[key]
        except KeyError:
            return None

        # Activate this constraint
        self.is_active = True

        if isinstance(value, kwtype):
            # value already correct type, return
            return value

        try:  # Try to convert value
            # Is this value one of the datetime types?
            if kwtype == datetime.date:
                time = datetime.datetime.strptime(value, "%Y-%m-%d")
                return datetime.date(time.year, time.month, time.day)

            if kwtype == datetime.datetime:
                return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

            return kwtype(value)
        except (TypeError, ValueError):
            raise SyntaxError("%s is not a %s" % (key, str(kwtype)))

    def is_valid(self, value):
        if not self.is_active:
            return None

        if not self._is_valid(value):
            return self._fail(value)

        return None

    def is_valid_path(self, value):
        if not self.is_active:
            return None

        if not self._is_valid_path(value):
            return self._fail_path(value)

        return None

    def _fail(self, value):
        return "'%s' violates %s." % (value, self.__class__.__name__)

    def _fail_path(self, value):
        return "'%s' violates %s." % (value, self.__class__.__name__)


class Min(Constraint):
    fail = "%s is less than %s"

    def __init__(self, value_type, kwargs):
        self.keywords = {"min": value_type}
        super(Min, self).__init__(value_type, kwargs)

    def _is_valid(self, value):
        return self.min <= value

    def _fail(self, value):
        return self.fail % (value, self.min)


class Max(Constraint):
    fail = "%s is greater than %s"

    def __init__(self, value_type, kwargs):
        self.keywords = {"max": value_type}
        super(Max, self).__init__(value_type, kwargs)

    def _is_valid(self, value):
        return self.max >= value

    def _fail(self, value):
        return self.fail % (value, self.max)


class LengthMin(Constraint):
    keywords = {"min": int}
    fail = "Length of %s is less than %s"

    def _is_valid(self, value):
        return self.min <= len(value)

    def _fail(self, value):
        return self.fail % (value, self.min)


class LengthMax(Constraint):
    keywords = {"max": int}
    fail = "Length of %s is greater than %s"

    def _is_valid(self, value):
        return self.max >= len(value)

    def _fail(self, value):
        return self.fail % (value, self.max)


class Key(Constraint):
    keywords = {"key": Validator}
    fail = "Key error - %s"

    def _is_valid(self, value):
        for k in value.keys():
            if self.key.validate(k) != []:
                return False
        return True

    def _fail(self, value):
        error_list = []
        for k in value.keys():
            error_list.extend(self.key.validate(k))
        return [self.fail % (e) for e in error_list]


class StringEquals(Constraint):
    keywords = {"equals": str, "ignore_case": bool}
    fail = "'%s' does not equal '%s'"

    def _is_valid(self, value):
        # Check if the function has only been called due to ignore_case
        if self.equals is not None:
            if self.ignore_case is not None:
                if not self.ignore_case:
                    return value == self.equals
                else:
                    return value.casefold() == self.equals.casefold()
            else:
                return value == self.equals
        else:
            return True

    def _fail(self, value):
        return self.fail % (value, self.equals)


class StringStartsWith(Constraint):
    keywords = {"starts_with": str, "ignore_case": bool}
    fail = "'%s' does not start with '%s'"

    def _is_valid(self, value):
        # Check if the function has only been called due to ignore_case
        if self.starts_with is not None:
            if self.ignore_case is not None:
                if not self.ignore_case:
                    return value.startswith(self.starts_with)
                else:
                    length = len(self.starts_with)
                    if length <= len(value):
                        return value[:length].casefold() == self.starts_with.casefold()
                    else:
                        return False
            else:
                return value.startswith(self.starts_with)
        else:
            return True

    def _fail(self, value):
        return self.fail % (value, self.starts_with)


class StringEndsWith(Constraint):
    keywords = {"ends_with": str, "ignore_case": bool}
    fail = "'%s' does not end with '%s'"

    def _is_valid(self, value):
        # Check if the function has only been called due to ignore_case
        if self.ends_with is not None:
            if self.ignore_case is not None:
                if not self.ignore_case:
                    return value.endswith(self.ends_with)
                else:
                    length = len(self.ends_with)
                    if length <= len(value):
                        return value[-length:].casefold() == self.ends_with.casefold()
                    else:
                        return False
            else:
                return value.endswith(self.ends_with)
        else:
            return True

    def _fail(self, value):
        return self.fail % (value, self.ends_with)


class StringMatches(Constraint):
    keywords = {"matches": str}

    _regex_flags = {"ignore_case": re.I, "multiline": re.M, "dotall": re.S}

    def __init__(self, value_type, kwargs):
        self._flags = 0
        for k, v in util.get_iter(self._regex_flags):
            self._flags |= v if kwargs.pop(k, False) else 0

        super(StringMatches, self).__init__(value_type, kwargs)

    def _is_valid(self, value):
        if self.matches is not None:
            regex = re.compile(self.matches, self._flags)
            return regex.match(value)
        else:
            return True

    def _fail(self, value):
        flags = []
        for flag in self._regex_flags.keys():
            if self._flags & self._regex_flags[flag]:
              flags += flag
        return "'%s' is not a regex match '%s' %s" % (value, self.matches, ', '.join(flags) )


class CharacterExclude(Constraint):
    keywords = {"exclude": str, "ignore_case": bool}
    fail = "'%s' contains excluded character '%s'"

    def _is_valid(self, value):
        # Check if the function has only been called due to ignore_case
        if self.exclude is not None:
            for char in self.exclude:
                if self.ignore_case is not None:
                    if not self.ignore_case:
                        if char in value:
                            self._failed_char = char
                            return False
                    else:
                        if char.casefold() in value.casefold():
                            self._failed_char = char
                            return False
                else:
                    if char in value:
                        self._failed_char = char
                        return False
            return True
        else:
            return True

    def _fail(self, value):
        return self.fail % (value, self._failed_char)


class IpVersion(Constraint):
    keywords = {"version": int}
    fail = "IP version of %s is not %s"

    def _is_valid(self, value):
        try:
            ip = ipaddress.ip_interface(to_unicode(value))
        except ValueError:
            return False
        return self.version == ip.version

    def _fail(self, value):
        return self.fail % (value, self.version)


class KeywordList_meta(type):
    def __str__(self):
        return f"one of {self.keywords}"

def KeywordList_class( *keyword_list ):
    class KeywordList(metaclass=KeywordList_meta):
        keywords = keyword_list

        def __init__(self, value):
            self.keyword = value.lower()
            if self.keyword not in self.keywords:
                raise ValueError

    return KeywordList

class IpPrefix(Constraint):
    keywords = {"prefix": KeywordList_class('length', 'mask', 'any', 'none') }

    def _is_valid(self, value):
        return (    self.prefix         == None
                 or self.prefix.keyword == 'length' and bool(re.match( r'^[^/]+/[0-9]+$',            value ))
                 or self.prefix.keyword == 'mask'   and bool(re.match( r'^[^/]+/([0-9]+\.)+[0-9]+$', value ))
                 or self.prefix.keyword == 'any'    and bool(re.match( r'^[^/]+/[0-9.]+$',           value ))
                 or self.prefix.keyword == 'none'   and bool(re.match( r'^[^/]+$',                   value ))
               )

    def _fail(self, value):
        return "IP prefix of %s is not '%s'" % (value, self.prefix.keyword)


class Validator_or_String:
    def __init__(self, value):
        self.value = value

    def validate( self, value ):
        if   isinstance( self.value, Validator ):
            result = ( [] == self.value.validate( value ) )
        elif type(self.value) is type(value):
            result =         self.value == value
        elif isinstance( self.value, str ):
            result =         self.value == str(value)
        else:
            result = False
        return result


class NodeName(Constraint):
    pre_check = True
    universal = True
    keywords  = {"name": Validator_or_String}

    def _is_valid_path(self, path):
        result = self.name.validate( path._path[-1] if len(path._path) > 0 else '<document>' )
        return result

    def _fail_path(self, path):
        return [ "Node name '%s' is not '%s'" % ( (path._path[-1] if len(path._path) > 0 else '<document>'), str(self.name.value) ) ]


class FileLine(Constraint):
    keywords = {   "method"     : KeywordList_class('equals', 'contains', 'starts_with', 'ends_with')
                 , "filename"   : list
                 , "encoding"   : str
                 , "ignore_case": bool
                 , "matches"    : str
                 , "replace"    : str

                 , "found"      : str
                 , "not_found"  : str
               }

    def _is_valid(self, value):
        method      = self.method.keyword if self.method      else 'equals'
        ignore_case = self.ignore_case    if self.ignore_case else False
        matches     = self.matches        if self.matches     else '^.*$'
        replace     = self.replace        if self.replace     else r'\g<0>'
        encoding    = self.encoding

        def exists_encoding( encoding ):
            try:
                import codecs
                codecs.lookup( encoding )
            except LookupError:
                return False
            return True

        def detect_encoding(file_path):
            with open(file_path, 'rb') as f:
                raw = f.read(4)
                if raw.startswith(b'\xef\xbb\xbf'):
                    return 'utf-8-sig'
                elif raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):  #  UTF-16LE or UTF-16BE
                    return 'utf-16'
                else:
                  #  try:
                  #      raw.decode('ascii')
                  #      return 'ascii'
                  #  except UnicodeDecodeError:
                        return 'utf-8'

        self.error = ''
        target, count = re.subn( matches, replace, value )
        if count < 1:
            self.error = f"{value} does not match to '{matches}'"
        else:
            target = value.lower() if ignore_case else target
            match  = not self.filename
            for fn in    self.filename:
                if not self.encoding or not exists_encoding(self.encoding):
                    encoding = detect_encoding( fn )
                raw = target.encode(encoding=encoding).decode(encoding=encoding, errors='surrogateescape')
                with open( fn, 'r', encoding=encoding, errors='surrogateescape' ) as f:
                    for line in f:
                        text = line.replace("\n", "")
                        if ignore_case:
                            text = text.lower()

                        match = (    method == "equals"      and raw == text
                                  or method == "contains"    and raw in text
                                  or method == "starts_with" and text.startswith(raw)
                                  or method == "ends_with"   and text.endswith(raw)
                                )
                        if match:
                            break
                    else:
                      continue
                    break
            if not match:
                self.error = f"{value} not found in {', '.join(self.filename)} by {method=} as '{target}'"
                if self.not_found:
                    with open( self.not_found, 'a+', encoding=encoding ) as f:
                        f.write( f"{value}\n" )
            else:
                if self.found:
                    with open( self.found, 'a+', encoding=encoding ) as f:
                        f.write( f"{value}\n" )
        return not self.error

    def _fail(self, value):
        return self.error
