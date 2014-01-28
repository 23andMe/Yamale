from __future__ import absolute_import
from .. import validators
try:
    import yaml
except ImportError:
    raise ImportError('You must install the pyyaml package '
                      'to validate YAML files')


def parse_file(file_name):
    with open(file_name) as f:
        return yaml.load(f)


def _parse_args(arg_string, **kwargs):
    args = []
    arg_list = arg_string.split()
    for arg in arg_list:
        if '=' in arg:
            key, sep, val = arg.partition('=')
            kwargs[key] = val
        elif '?' in arg:
            pass
        else:
            args.append(arg)
    return args, kwargs


def _get_type(arg_string):
    return arg_string.split()[0][1:]


def _multi_constructor_factory(required=True):
    def multi_constructor(loader, tag, node):
        arg_string = loader.construct_scalar(node)
        args, kwargs = _parse_args(arg_string, required=required)
        if not required:
            tag = _get_type(arg_string)
        for validator in validators.TYPES:
            if tag == validator.__tag__:
                return validator(*args, **kwargs)
        raise ValueError('Validator "%s" with arguments [%s] is not recognized.' % (tag, arg_string))
    return multi_constructor

yaml.add_multi_constructor('!', _multi_constructor_factory())
yaml.add_multi_constructor('?', _multi_constructor_factory(required=False))

import re
optional = re.compile(r'^\?\w+')
yaml.add_implicit_resolver(u'?', optional)
