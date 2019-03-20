from __future__ import absolute_import


def _pyyaml(file_name, constructors=None):
    import yaml
    try:
        if constructors is not None:
            Loader = yaml.Loader
            for c in constructors:
                yaml.add_constructor(c[0],c[1])
        else:
            Loader = yaml.CSafeLoader
    except AttributeError:  # System does not have libyaml
        Loader = yaml.SafeLoader
    with open(file_name) as f:
        return list(yaml.load_all(f, Loader=Loader))


def _ruamel(file_name, constructors=None):
    from ruamel.yaml import YAML
    yaml = YAML(typ='safe')
    with open(file_name) as f:
        return list(yaml.load_all(f))


_parsers = {
    'pyyaml': _pyyaml,
    'ruamel': _ruamel
}


def parse_file(file_name, parser, constructors=None):
    try:
        parse = _parsers[parser.lower()]
    except KeyError:
        raise NameError('Parser "' + parser + '" is not supported\nAvailable parsers are listed below:\nPyYAML\nruamel')
    return parse(file_name, constructors)
