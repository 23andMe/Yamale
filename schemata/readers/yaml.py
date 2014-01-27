from __future__ import absolute_import
try:
    import yaml
except ImportError:
    raise ImportError('You must install the pyyaml package '
                      'to validate YAML files')


def parse_file(file_name):
    with open(file_name) as f:
        return yaml.load(f)


def constructor_factory(validator):
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return validator(value.split())
    return '!' + validator.__tag__, constructor

from ..validators.string import String
yaml.add_constructor(*constructor_factory(String))
