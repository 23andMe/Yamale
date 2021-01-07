from __future__ import absolute_import
import yaml
from io import StringIO

class NoDatesSafeLoader(yaml.SafeLoader):
    @classmethod
    def remove_implicit_resolver(cls, tag_to_remove):
        """
        Remove implicit resolvers for a particular tag
        Takes care not to modify resolvers in super classes.

        We want to load datetimes as strings, not dates, so that we 
        can test the format constraint. 
        """
        if not 'yaml_implicit_resolvers' in cls.__dict__:
            cls.yaml_implicit_resolvers = cls.yaml_implicit_resolvers.copy()

        for first_letter, mappings in cls.yaml_implicit_resolvers.items():
            cls.yaml_implicit_resolvers[first_letter] = [(tag, regexp) 
                                                         for tag, regexp in mappings
                                                         if tag != tag_to_remove]

NoDatesSafeLoader.remove_implicit_resolver('tag:yaml.org,2002:timestamp')


def _pyyaml(f):
    try:
        Loader = NoDatesSafeLoader
    except: 
        try: 
            Loader = yaml.CSafeLoader
        except AttributeError:  # System does not have libyaml
            Loader = yaml.SafeLoader
    return list(yaml.load_all(f, Loader=Loader))


def _ruamel(f):
    from ruamel.yaml import YAML
    yaml = YAML(typ='safe')
    
    # Replace timestamp constructor to prevent converting to datetime obj
    yaml.constructor.yaml_constructors[u'tag:yaml.org,2002:timestamp'] = \
        yaml.constructor.yaml_constructors[u'tag:yaml.org,2002:str']

    return list(yaml.load_all(f))


_parsers = {
    'pyyaml': _pyyaml,
    'ruamel': _ruamel
}


def parse_yaml(path=None, parser='pyyaml', content=None):
    try:
        parse = _parsers[parser.lower()]
    except KeyError:
        raise NameError('Parser "' + parser + '" is not supported\nAvailable parsers are listed below:\nPyYAML\nruamel')
    if (path is None and content is None) or (path is not None and content is not None):
        raise TypeError("Pass either path= or content=, not both")
    if path is not None:
        with open(path) as f:
            return parse(f)
    else:
        return parse(StringIO(content))
