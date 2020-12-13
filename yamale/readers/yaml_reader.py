from __future__ import absolute_import
import yaml

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
    return list(yaml.load_all(f, Loader=NoDatesSafeLoader))


def _ruamel(file_name):
    from ruamel.yaml import YAML
    yaml = YAML(typ='safe')
    # Replace timestamp constructor to prevent converting to datetime obj
    yaml.constructor.yaml_constructors[u'tag:yaml.org,2002:timestamp'] = \
        yaml.constructor.yaml_constructors[u'tag:yaml.org,2002:str']
    with open(file_name) as f:
        return list(yaml.load_all(f))


_parsers = {
    'pyyaml': _pyyaml,
    'ruamel': _ruamel
}


def parse_file(file_name, parser):
    try:
        parse = _parsers[parser.lower()]
    except KeyError:
        raise NameError('Parser "' + parser + '" is not supported\nAvailable parsers are listed below:\nPyYAML\nruamel')
    return parse(file_name)
