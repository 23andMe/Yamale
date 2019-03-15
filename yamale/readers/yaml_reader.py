from __future__ import absolute_import

from yamale import util


def _pyyaml(file_name):
    import yaml
    try:
        Loader = yaml.CSafeLoader
    except AttributeError:  # System does not have libyaml
        Loader = yaml.SafeLoader
    with open(file_name) as f:
        return list(yaml.load_all(f, Loader=Loader))


def _ruamel(file_name):
    from ruamel.yaml import YAML
    yaml = YAML(typ='safe')
    with open(file_name) as f:
        return list(yaml.load_all(f))


_parsers = {
    'pyyaml': _pyyaml,
    'ruamel': _ruamel
}


def _munge_keys(dic, old_string, new_string):
    munged_dict = {}
    for k, v in util.get_iter(dic):
        if isinstance(v, dict):
            v = _munge_keys(v, old_string, new_string)
        if util.isstr(k):
            munged_dict[k.replace(old_string, new_string)] = v
        else:
            munged_dict[k] = v
    return munged_dict


def parse_file(file_name, parser):
    try:
        parse = _parsers[parser.lower()]
    except KeyError:
        raise NameError('Parser "' + parser + '" is not supported\nAvailable parsers are listed below:\nPyYAML\nruamel')
    yaml_documents = []
    parsed_file = parse(file_name)
    for document in parsed_file:
        yaml_documents.append(_munge_keys(document, '.', '_'))
    return yaml_documents
