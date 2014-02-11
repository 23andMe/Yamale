from . import yaml
from . import json

readers = {
    'yaml': yaml.parse_file,
    'yml': yaml.parse_file,
    'json': json.parse_file
}


def parse_file(path, reader=None):
    if reader is None:
        reader = _guess_reader(path)
    try:
        return readers[reader](path)
    except KeyError:
        raise ValueError('Reader "%s" not recognized.' % reader)


def _guess_reader(path):
    '''
    TOP SECRET.
    Super advanced file type detection algorithm.
    Default to yaml.
    '''
    t = path.split('.')[-1]
    if t not in readers:
        t = 'yaml'
    return t
