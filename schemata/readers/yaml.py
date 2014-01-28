from __future__ import absolute_import
try:
    import yaml
except ImportError:
    raise ImportError('You must install the pyyaml package '
                      'to validate YAML files')

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def parse_file(file_name):
    with open(file_name) as f:
        return yaml.load(f, Loader=Loader)
