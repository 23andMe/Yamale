import ast

from .. import validators as val


def _validate_expr(call_node, validators):
    # Validate that the expression uses a known, registered validator.
    try:
        func_name = call_node.func.id
    except AttributeError:
        raise SyntaxError("Schema expressions must be enclosed by a validator.")
    if func_name not in validators:
        raise SyntaxError("Not a registered validator: '%s'. " % func_name)
    # Validate that all args are constant literals, validator names, or other call nodes
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


def _eval_literal(node, validators):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name) and node.id in validators:
        return validators[node.id]
    if isinstance(node, ast.UnaryOp) and isinstance(node.operand, ast.Constant):
        value = node.operand.value
        if isinstance(node.op, ast.UAdd):
            return +value
        if isinstance(node.op, ast.USub):
            return -value
        if isinstance(node.op, ast.Not):
            return not value
        if isinstance(node.op, ast.Invert):
            return ~value
    if isinstance(node, ast.Call):
        return _construct_validator(node, validators)
    raise SyntaxError("Argument values must either be constant literals, or else reference other validators.")


def _construct_validator(call_node, validators):
    func_name = call_node.func.id
    args = [_eval_literal(arg, validators) for arg in call_node.args]
    kwargs = {}
    for keyword in call_node.keywords:
        if keyword.arg is None:
            raise SyntaxError("Keyword argument unpacking is not supported.")
        kwargs[keyword.arg] = _eval_literal(keyword.value, validators)
    return validators[func_name](*args, **kwargs)


def parse(validator_string, validators=None):
    validators = validators or val.DefaultValidators
    try:
        tree = ast.parse(validator_string, mode="eval")
        _validate_expr(tree.body, validators)
        return _construct_validator(tree.body, validators)
    except (SyntaxError, NameError, TypeError) as e:
        raise SyntaxError("Invalid schema expression: '%s'. " % validator_string + str(e))
