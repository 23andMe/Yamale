import ast


safe_globals = ('True', 'False', 'None')
safe_builtins = dict((f, __builtins__[f]) for f in safe_globals)


def parse(validator_string, validators):
    try:
        tree = ast.parse(validator_string, mode='eval')
        # evaluate with access to a limited global scope only
        return eval(
            compile(tree, '<ast>', 'eval'),
            {'__builtins__': safe_builtins},
            validators
            )
    except (SyntaxError, NameError, TypeError) as e:
        raise SyntaxError(
            'Invalid validation syntax in \'%s\', ' % validator_string +
            str(e)
        )
