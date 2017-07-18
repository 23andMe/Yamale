#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Validate yaml files and check them against their schemas. Designed to be used outside of Vagrant.

    Just install Yamale:
        pip install yamale
"""

import argparse
import glob
import os
from multiprocessing import Pool

import yamale

schemas = {}


def _validate(schema_path, data_path):
    schema = schemas.get(schema_path)
    if not schema:
        schema = yamale.make_schema(schema_path)
        schemas[schema_path] = schema
    data = yamale.make_data(data_path)
    yamale.validate(schema, data)


def _find_schema(data_path, schema_name):
    '''Find if the schema file exists. If not, look for all files
    that match the expression of "schema_name" and if no file is
    found try the same in data_path directory. Only the first file
    is returned. 
    
    Return a valid path or raise error if no file is found.'''

    if os.path.isfile(schema_name):
        return schema_name
    else:
        path = glob.glob(schema_name)
        if len(path) == 0:
            if data_path and data_path != '/' and data_path != '.':
                directory = os.path.dirname(data_path)
                path = glob.glob(os.path.join(directory, schema_name))
        
        if len(path) > 0:
            path = [ p for p in path if os.path.isfile(p)][0]
        else:
            raise ValueError("Invalid schema name for '{}' or schema not found.".format(schema_name))

    return path


def _validate_single(yaml_path, schema_name):
    print('Validating %s...' % yaml_path)
    s = _find_schema(yaml_path, schema_name)
    _validate(s, yaml_path)


def _validate_dir(root, schema_name, cpus):
    pool = Pool(processes=cpus)
    res = []
    print('Finding yaml files...')
    for root, dirs, files in os.walk(root):
        for f in files:
            if f.endswith('.yaml') or f.endswith('.yml') and f != schema_name:
                d = os.path.join(root, f)
                s = _find_schema(d, schema_name)
                if s:
                    res.append(pool.apply_async(_validate, (s, d)))
                else:
                    print('No schema found for: %s' % d)

    print('Found %s yaml files.' % len(res))
    print('Validating...')
    for r in res:
        r.get(timeout=300)
    pool.close()
    pool.join()


def _router(root, schema_name, cpus):
    root = os.path.abspath(root)
    if root.endswith('.yaml') or root.endswith('.yml'):
        _validate_single(root, schema_name)
    else:
        _validate_dir(root, schema_name, cpus)


def main():
    parser = argparse.ArgumentParser(description='Validate yaml files.')
    parser.add_argument('path', metavar='PATH', default='./', nargs='?',
                        help='folder to validate. Default is current directory.')
    parser.add_argument('-s', '--schema', default='schema.yaml',
                        help='filename of schema. Default is schema.yaml.')
    parser.add_argument('-n', '--cpu-num', default=4, type=int,
                        help='number of CPUs to use. Default is 4.')
    args = parser.parse_args()
    _router(args.path, args.schema, args.cpu_num)
    print('Validation success! 👍')


if __name__ == '__main__':
    main()
