from schemata import validators as val


tags = {v.__tag__: v for v in val.TYPES}


def parse(validator_string):
    try:
        return tags[validator_string.replace('()', '')]()
    except KeyError:
        raise SyntaxError
