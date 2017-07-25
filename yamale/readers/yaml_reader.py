from __future__ import absolute_import

def parse_file(file_name, parser):
    if 'PyYAML' == parser:
        import yaml
        try:
            Loader = yaml.CSafeLoader
        except AttributeError:  # System does not have libyaml
            Loader = yaml.SafeLoader
        with open(file_name) as f:
            return list(yaml.load_all(f, Loader=Loader))

    elif 'ruamel' == parser:
        from ruamel.yaml import YAML
        yaml=YAML(typ='safe')
        with open(file_name) as f:
            return list(yaml.load_all(f))

    else:
        raise NameError('Parser "' + parser + '" is not supported\nAvailable parsers are listed below:\nPyYAML\nruamel')
