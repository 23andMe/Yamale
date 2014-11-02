from __future__ import absolute_import
import yaml

try:
    Loader = yaml.CSafeLoader
except AttributeError:  # System does not have libyaml
    Loader = yaml.SafeLoader


def parse_file(file_name):
    with open(file_name) as f:
        return list(yaml.load_all(f, Loader=Loader))
