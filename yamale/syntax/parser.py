import ast

from .. import validators as val

safe_globals = ("True", "False", "None" )
safe_builtins = dict((f, __builtins__[f]) for f in safe_globals)

def _validate_expr(call_node, validators):
    # Validate that the expression uses a known, registered validator.
    try:
        func_name = call_node.func.id
    except AttributeError:
        raise SyntaxError("Schema expressions must be enclosed by a validator.")
    if func_name not in validators:
        raise SyntaxError("Not a registered validator: '%s'. " % func_name)
    # Validate that all args are constant literals, validator names,  or other call nodes
    arg_values = call_node.args + [kw.value for kw in call_node.keywords]
    for arg in arg_values:
        base_arg = arg.operand if isinstance(arg, ast.UnaryOp) else arg
        if isinstance(base_arg, ast.Constant):
            continue
        elif isinstance(base_arg, ast.Name) and base_arg.id in validators:
            continue
        elif isinstance(base_arg, ast.Call):
            _validate_expr(base_arg, validators)
        else:
            raise SyntaxError("Argument values must either be constant literals, or else " "reference other validators.")


def parse(validator_string, validators=None):
    validators = validators or val.DefaultValidators
    try:
        import datetime
        if validator_string == None:
          tree = ast.parse( f"null()", mode="eval")
        elif isinstance( validator_string, datetime.datetime ):
          tree = ast.parse( f"timestamp('{str(validator_string)}')", mode="eval")
        elif isinstance( validator_string, datetime.date ):
          tree = ast.parse( f"day('{str(validator_string)}')", mode="eval")
        elif not isinstance(validator_string,str):
          tree = ast.parse( f"enum({repr(validator_string)})", mode="eval")
        else:
          tree = ast.parse( validator_string, mode="eval")
        _validate_expr(tree.body, validators)
        # evaluate with access to a limited global scope only
        return eval(compile(tree, "<ast>", "eval"), {"__builtins__": safe_builtins}, validators)
    except (SyntaxError, NameError, TypeError) as e:
        raise SyntaxError("Invalid schema expression: '%s' %s: %s" % (repr(validator_string), type(validator_string), str(e)) )
