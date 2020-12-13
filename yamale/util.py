# ABCs for containers were moved to their own module
try:
    from collections.abc import Mapping, Set, Sequence
except ImportError:
    from collections import Mapping, Set, Sequence


# Python 3 has no basestring, lets test it.
try:
    basestring  # attempt to evaluate basestring

    def isstr(s):
        return isinstance(s, basestring)

    def to_unicode(s):
        return unicode(s)

except NameError:
    def isstr(s):
        return isinstance(s, str)

    def to_unicode(s):
        return s


def is_list(obj):
    return isinstance(obj, Sequence) and not isstr(obj)


def is_map(obj):
    return isinstance(obj, Mapping)


def get_keys(obj):
    if is_map(obj):
        return obj.keys()
    elif is_list(obj):
        return range(len(obj))


def get_iter(iterable):
    if isinstance(iterable, Mapping):
        return iterable.items()
    else:
        return enumerate(iterable)


def get_subclasses(cls, _subclasses_yielded=None):
    """
    Generator recursively yielding all subclasses of the passed class (in
    depth-first order).

    Parameters
    ----------
    cls : type
        Class to find all subclasses of.
    _subclasses_yielded : set
        Private parameter intended to be passed only by recursive invocations of
        this function, containing all previously yielded classes.
    """

    if _subclasses_yielded is None:
        _subclasses_yielded = set()

    # If the passed class is old- rather than new-style, raise an exception.
    if not hasattr(cls, '__subclasses__'):
        raise TypeError('Old-style class "%s" unsupported.' % cls.__name__)

    # For each direct subclass of this class
    for subclass in cls.__subclasses__():
        # If this subclass has already been yielded, skip to the next.
        if subclass in _subclasses_yielded:
            continue

        # Yield this subclass and record having done so before recursing.
        yield subclass
        _subclasses_yielded.add(subclass)

        # Yield all direct subclasses of this class as well.
        for subclass_subclass in get_subclasses(subclass, _subclasses_yielded):
            yield subclass_subclass


class InvalidDatetimeValue(Exception):
    """ Custom exception for date and datetime values that 
    cannot be parsed without custom format parameter.
    """
    pass


def parse_default_date(value):
    """
    This method parses day and timestamp values if no format is passed 
    as a constraint. This is to ensure values are consistent as they 
    would be if using the default PyYAML and ruamel loaders. 

    Parameters
    ----------
    value : string
    """
    import re
    import datetime

    # Regex from PyYAML constructor.py ln 310
    timestamp_regexp = re.compile(
            r'''^(?P<year>[0-9][0-9][0-9][0-9])
                -(?P<month>[0-9][0-9]?)
                -(?P<day>[0-9][0-9]?)
                (?:(?:[Tt]|[ \t]+)
                (?P<hour>[0-9][0-9]?)
                :(?P<minute>[0-9][0-9])
                :(?P<second>[0-9][0-9])
                (?:\.(?P<fraction>[0-9]*))?
                (?:[ \t]*(?P<tz>Z|(?P<tz_sign>[-+])(?P<tz_hour>[0-9][0-9]?)
                (?::(?P<tz_minute>[0-9][0-9]))?))?)?$''', re.X)

    match = timestamp_regexp.match(value)
    
    if match:
        values = match.groupdict()
        year = int(values['year'])
        month = int(values['month'])
        day = int(values['day'])
        if not values['hour']:
            return datetime.date(year, month, day)
        hour = int(values['hour'])
        minute = int(values['minute'])
        second = int(values['second'])
        fraction = 0
        tzinfo = None
        if values['fraction']:
            fraction = values['fraction'][:6]
            while len(fraction) < 6:
                fraction += '0'
            fraction = int(fraction)
        if values['tz_sign']:
            tz_hour = int(values['tz_hour'])
            tz_minute = int(values['tz_minute'] or 0)
            delta = datetime.timedelta(hours=tz_hour, minutes=tz_minute)
            if values['tz_sign'] == '-':
                delta = -delta
            tzinfo = datetime.timezone(delta)
        elif values['tz']:
            tzinfo = datetime.timezone.utc
        return datetime.datetime(year, month, day, hour, minute, second, fraction,
                                    tzinfo=tzinfo)
    else: 
        raise InvalidDatetimeValue('Datetime value is not in standard ISO 8601 format.')
