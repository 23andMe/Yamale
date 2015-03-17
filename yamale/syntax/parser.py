import ast

from .. import validators as val

safe_globals = ('True', 'False', 'None')
safe_builtins = dict((f, __builtins__[f]) for f in safe_globals)


def parse(validator_string, validators=None):
    validators = validators or val.DefaultValidators
    try:
        tree = ast.parse(validator_string, mode='eval')
        # evaluate with access to a limited global scope only
        return eval(compile(tree, '<ast>', 'eval'),
                    {'__builtins__': safe_builtins},
                    validators)
    except (SyntaxError, NameError, TypeError) as e:
        raise SyntaxError(
            'Invalid schema expression: \'%s\'. ' % validator_string +
            str(e)
        )
