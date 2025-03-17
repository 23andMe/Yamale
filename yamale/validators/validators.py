import re
import datetime
import dateutil.parser
import ipaddress
from .base import Validator
from . import constraints as con
from .. import util
from .. import yamale

# ABCs for containers were moved to their own module
try:
    from collections.abc import Sequence, Mapping
except ImportError:
    from collections import Sequence, Mapping


class String(Validator):
    """String validator"""

    value_type = str
    tag = "str"
    constraints = [
        con.LengthMin,
        con.LengthMax,
        con.CharacterExclude,
        con.StringEquals,
        con.StringStartsWith,
        con.StringEndsWith,
        con.StringMatches,
    ]

    def __init__(self, *args, **kwargs):
        super(String, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        if (    not isinstance(value, str)
             or isinstance(value, bool)
             or self.args and value not in self.args
           ):
            self.error = "'%s' is not a %s(%s,%s)" % ( value, self.__class__.__name__, self.args, self.kwargs )
            return False
        return True

    def fail(self, value):
        return self.error



class Number(Validator):
    """Number/float validator"""

    value_type = float
    tag = "num"
    constraints = [con.Min, con.Max]

    def __init__(self, *args, **kwargs):
        super(Number, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        if (    not isinstance(value, (int, float))
             or isinstance(value, bool)
             or self.args and value not in self.args
           ):
            self.error = "'%s' is not a %s(%s,%s)" % ( value, self.__class__.__name__, self.args, self.kwargs )
            return False
        return True

    def fail(self, value):
        return self.error


class Integer(Validator):
    """Integer validator"""

    value_type = int
    tag = "int"
    constraints = [con.Min, con.Max]

    def __init__(self, *args, **kwargs):
        super(Integer, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        if (    not isinstance(value, int)
             or isinstance(value, bool)
             or self.args and value not in self.args
           ):
            self.error = "'%s' is not a %s(%s,%s)" % ( value, self.__class__.__name__, self.args, self.kwargs )
            return False
        return True

    def fail(self, value):
        return self.error


class Boolean(Validator):
    """Boolean validator"""

    tag = "bool"

    def __init__(self, *args, **kwargs):
        super(Boolean, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        if (    not isinstance(value, bool)
             or self.args and value not in self.args
           ):
            self.error = "'%s' is not a %s(%s,%s)" % ( value, self.__class__.__name__, self.args, self.kwargs )
            return False
        return True

    def fail(self, value):
        return self.error


class Enum(Validator):
    """Enum validator"""

    tag = "enum"

    def __init__(self, *args, **kwargs):
        super(Enum, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        return value in self.args

    def fail(self, value):
        return "'%s' not in %s" % (value, self.args)


class Day(Validator):
    """Day validator. Format: YYYY-MM-DD"""

    value_type = datetime.date
    tag = "day"
    constraints = [con.Min, con.Max]

    def __init__(self, *args, **kwargs):
        args = [ dateutil.parser.parse( arg ).date() for arg in args ]
        super(Day, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        if (    not isinstance(value, datetime.date)
             or self.args and value not in self.args
           ):
            self.error = "'%s' is not a %s(%s,%s)" % ( value, self.__class__.__name__, self.args, self.kwargs )
            return False
        return True

    def fail(self, value):
        return self.error


class Timestamp(Validator):
    """Timestamp validator. Format: YYYY-MM-DD HH:MM:SS"""

    value_type = datetime.datetime
    tag = "timestamp"
    constraints = [con.Min, con.Max]

    def __init__(self, *args, **kwargs):
        args = [ dateutil.parser.parse( arg )  for arg in args ]
        super(Timestamp, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        if (    not isinstance(value, datetime.datetime)
             or self.args and value not in self.args
           ):
            self.error = "'%s' is not a %s(%s,%s)" % ( value, self.__class__.__name__, self.args, self.kwargs )
            return False
        return True

    def fail(self, value):
        return self.error


class Map(Validator):
    """Map and dict validator"""

    tag = "map"
    constraints = [con.LengthMin, con.LengthMax, con.Key]

    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        self.validators = [val for val in args if isinstance(val, Validator)]

    def _is_valid(self, value):
        return isinstance(value, Mapping)


class List(Validator):
    """List validator"""

    tag = "list"
    constraints = [con.LengthMin, con.LengthMax]

    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
        self.validators = [val for val in args if isinstance(val, Validator)]

    def _is_valid(self, value):
        return isinstance(value, Sequence) and not util.isstr(value)


class Include(Validator):
    """Include validator"""

    tag = "include"

    def __init__(self, *args, **kwargs):
        self.include_name = args[0]
        self.strict       = kwargs.pop("strict", None)
        super(Include, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        if isinstance( value, dict ) or isinstance( value, list ):
            return True

        self.errors = []
        try:
            for err in yamale.schema.includes[self.include_name].validate( value, self.include_name, self.strict ).errors:
               if isinstance(err, list):
                 self.errors.extend(err)
               else:
                 self.errors.append(err)
        except KeyError:
            self.errors = [ f"'{self.include_name}' is not included" ]
        return not self.errors

    def get_name(self):
        return self.include_name

    def fail(self, value):
        return "'%s' is not %s because %s" % (value, self.include_name, '; '.join( self.errors ) )

class Any(Validator):
    """Any of several types validator"""

    tag = "any"

    def __init__(self, *args, **kwargs):
        self.literals   = []
        self.validators = []
        for val in args:
            if isinstance(val, Validator):
                self.validators.append( val )
            else:
                self.literals.append( val )

        if self.literals:
            self.validators.append( Enum( *self.literals ) )

        super(Any, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        if isinstance( value, dict ) or isinstance( value, list ):
            return True

        self.error = ''
        for v in self.validators:
            if v._is_valid(value):
                break
        else:
            self.error = "'%s' does not match %s(%s,%s)" % ( value, self.__class__.__name__, self.args, self.kwargs )

        return not self.error

    def fail(self, value):
        return self.error


class NotAny(Validator):
    """No one of several types validator"""

    tag = "notany"
 
    def __init__(self, *args, **kwargs):
        self.validators = Any( *args, **kwargs ).validators
        super(NotAny, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        if isinstance( value, dict ) or isinstance( value, list ):
            return True

        self.error = ''
        for v in self.validators:
            if v._is_valid(value):
                self.error =  "'%s' matches to %s(%s,%s)" % ( value, self.__class__.__name__, self.args, self.kwargs )
                break

        return not self.error

    def fail(self, value):
        return self.error


class All(Validator):
    """All of several types validator"""

    tag = "all"
 
    def __init__(self, *args, **kwargs):
        self.validators = Any( *args, **kwargs ).validators
        super(All, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        if isinstance( value, dict ) or isinstance( value, list ):
            return True

        self.error = ''
        for v in self.validators:
            if not v._is_valid(value):
                self.error =  "'%s' does not match to %s(%s,%s)" % ( value, self.__class__.__name__, self.args, self.kwargs )
                break

        return not self.error

    def fail(self, value):
        return self.error


class Subset(Validator):
    """Subset of several types validator"""

    tag = "subset"

    def __init__(self, *args, **kwargs):
        super(Subset, self).__init__(*args, **kwargs)
        self._allow_empty_set = bool(kwargs.pop("allow_empty", False))
        self.validators = [val for val in args if isinstance(val, Validator)]
        if not self.validators:
            raise ValueError("'%s' requires at least one validator!" % self.tag)

    def _is_valid(self, value):
        return self.can_be_none or value is not None

    def fail(self, value):
        # Called in case `_is_valid` returns False
        return "'%s' may not be an empty set." % self.get_name()

    @property
    def is_optional(self):
        return self._allow_empty_set

    @property
    def can_be_none(self):
        return self._allow_empty_set


class Null(Validator):
    """Validates null"""

    value_type = None
    tag = "null"

    def _is_valid(self, value):
        return value is None


class Regex(Validator):
    """Regular expression validator"""

    tag = "regex"
    _regex_flags = {"ignore_case": re.I, "multiline": re.M, "dotall": re.S}

    def __init__(self, *args, **kwargs):
        self.regex_name = kwargs.pop("name", None)

        flags = 0
        for k, v in util.get_iter(self._regex_flags):
            flags |= v if kwargs.pop(k, False) else 0

        self.regexes = [re.compile(arg, flags) for arg in args if util.isstr(arg)]
        super(Regex, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        return util.isstr(value) and any(r.match(value) for r in self.regexes)

    def get_name(self):
        return self.regex_name or self.tag + " match"


class Ip(Validator):
    """IP address validator"""

    tag = "ip"
    constraints = [con.IpVersion, con.IpPrefix]

    def __init__(self, *args, **kwargs):
        self.strict = bool(kwargs.get("strict", False))
        super(Ip, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        return self.ip_address(value)

    def ip_address(self, value):
        try:
            ip = ipaddress.ip_network(util.to_unicode(value), self.strict)
        except ValueError:
            return False
        return True

    def fail(self, value):
        return "'%s' is not ip(%s)" % (value, str(self.kwargs) )

class FQDN(Validator):
    """FQDN validator"""

    tag = 'fqdn'

    def __init__(self, *args, **kwargs):
        self.matches   = kwargs.get("matches", '^((?P<host>[^.]+)\.)?([^.]+\.)+[^.]+[.]?$') # hostname.domain.tld
        self.resolve   = kwargs.get("resolve", False)
        self.nameType  = kwargs.get("type", 'host')
        self.minLabels = kwargs.get("min", 2  )
        self.maxLabels = kwargs.get("max", 255)
        if self.nameType not in ( 'domain', 'host' ):
            raise ValueError( f"'{self.nameType}' is not one of ('domain', 'host')" )
        super(FQDN, self).__init__(*args, **kwargs)


    def is_valid_fqdn(self, fqdn ):
        if not isinstance(fqdn, str) or len(fqdn) < 1 or len(fqdn) > 254:
          return False
        try:
            import ipaddress
            ipaddress.ip_address(fqdn)
            return False
        except ValueError:
            pass

        if self.matches:
          match = re.match( self.matches, fqdn )
          if not match:
              return False

        if fqdn[-1] == ".":
            fqdn = fqdn[:-1]
        labels = fqdn.split(".")
        if len(labels) < self.minLabels or len(labels) > self.maxLabels:
            return False
        for l in labels:
            if len(l) < 1 or len(l) > 63:
              return False

        if self.resolve:
            is_domain = False
            is_host   = False
            try:
                import dns.resolver
                canon     = dns.resolver.canonical_name( fqdn+'.' )
                for t in ("SOA", "NS", "MX" ):
                    try:
                        dns.resolver.resolve(canon, t)
                        is_domain = True
                        break
                    except( dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers ):
                        pass
                for t in ("A", "AAAA"):
                    try:
                        dns.resolver.resolve(canon, t)
                        is_host = True
                        break
                    except( dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers ):
                        pass
            except( dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers ):
                pass

            return (    self.nameType == 'domain'    and is_domain
                     or self.nameType == 'host'      and is_host
                   )
        elif self.matches:
            res =  (    self.nameType == 'domain' and ( 'host' not in match.groupdict()  or  not match['host'] )
                     or self.nameType == 'host'   and ( 'host'     in match.groupdict()  and     match['host'] )
                   )
            return res
        return True

    def _is_valid(self, value):
       return self.is_valid_fqdn( value )

    def fail(self, value):
        return "'%s' is not fqdn(%s)" % (value, str(self.kwargs) )


class Mac(Regex):
    """MAC address validator"""

    tag = "mac"

    def __init__(self, *args, **kwargs):
        super(Mac, self).__init__(*args, **kwargs)
        self.regexes = [
            re.compile(r"[0-9a-fA-F]{2}([-:]?)[0-9a-fA-F]{2}(\1[0-9a-fA-F]{2}){4}$"),
            re.compile(r"[0-9a-fA-F]{4}([-:]?)[0-9a-fA-F]{4}(\1[0-9a-fA-F]{4})$"),
        ]


class SemVer(Regex):
    """Semantic Versioning (semver.org) validator"""

    tag = "semver"

    def __init__(self, *args, **kwargs):
        super(SemVer, self).__init__(*args, **kwargs)
        self.regexes = [
            # https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
            re.compile(
                r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
            ),
        ]

class FileLine(Validator):
    """checks if the value is in a file line"""

    tag = "file_line"

    constraints = [
        con.FileLine
    ]

    def __init__(self, *args, **kwargs):
        self.filename = args
        self.error    = ''
        super(FileLine, self).__init__(*args, **dict( kwargs, filename=args ))

    def _is_valid(self, value):
        from pathlib import Path
        for fn in self.filename:
          f = Path(fn)
          if not f.is_file():
            self.error = f"file '{fn}' does not exists"
        return not self.error

    def fail(self, value):
        return self.error


DefaultValidators = {}

for v in util.get_subclasses(Validator):
    # Allow validator nodes to contain either tags or actual name
    DefaultValidators[v.tag] = v
    DefaultValidators[v.__name__] = v
