import ast

from .. import validators as val

# Get all validators in here for eval()
from ..validators.validators import *

# Allow validator strings to contain either tags or actual name
tags = {v.tag: v.__name__ for v in val.TYPES}
tags.update({v.__name__: v.__name__ for v in val.TYPES})


def parse(validator_string):
    try:
        tree = ast.parse(validator_string, mode='eval')

        for node in ast.walk(tree):
            node = _process_node(tags, node)

        validator = eval(compile(tree, '<ast>', 'eval'))

        return validator
    except (KeyError, SyntaxError) as e:
        raise SyntaxError(
            'Invalid validation syntax in \'%s\', ' % validator_string +
            str(e)
        )


def _process_node(tags, node):
    if isinstance(node, ast.Call):
        # Only allow functions we list in `tags`.
        node.func.id = tags[node.func.id]
