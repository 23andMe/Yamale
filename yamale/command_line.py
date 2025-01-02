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
import re
import multiprocessing
from .yamale_error import YamaleError
from .schema.validationresults import Result
from .version import __version__

import yamale

schemas = {}


def _validate(schema_path, data_path, parser, strict, _raise_error):
    schema = schemas.get(schema_path)
    try:
        if not schema:
            schema = yamale.make_schema(schema_path, parser)
            schemas[schema_path] = schema
    except (SyntaxError, ValueError) as e:
        results = [Result([str(e)])]
        if not _raise_error:
            return results
        raise YamaleError(results)
    data = yamale.make_data(data_path, parser)
    return yamale.validate(schema, data, strict, _raise_error)


def _find_data_path_schema(data_path, schema_name):
    """Starts in the data file folder and recursively looks
    in parents for `schema_name`"""
    if not data_path or data_path == os.path.abspath(os.sep) or data_path == ".":
        return None
    directory = os.path.dirname(data_path)
    path = glob.glob(os.path.join(directory, schema_name))
    if not path:
        return _find_schema(directory, schema_name)
    return path[0]


def _find_schema(data_path, schema_name):
    """Checks if `schema_name` is a valid file, if not
    searches in `data_path` for it."""

    if os.path.isfile(schema_name):
        return schema_name

    directory = os.path.dirname(data_path)
    path = glob.glob(os.path.join(directory, schema_name))
    for p in path:
        if os.path.isfile(p):
            return p

    return _find_data_path_schema(data_path, schema_name)


def _validate_file(yaml_path, schema_name, parser, strict, should_exclude):
    if should_exclude(yaml_path):
        return
    s = _find_schema(yaml_path, schema_name)
    if not s:
        raise ValueError("Invalid schema name for '{}' or schema not found.".format(schema_name))
    _validate(s, yaml_path, parser, strict, True)


def _validate_dir(root, schema_name, cpus, parser, strict, should_exclude):
    pool = multiprocessing.Pool(processes=cpus)
    res = []
    error_messages = []
    for root, _, files in os.walk(root):
        for f in files:
            if (f.endswith(".yaml") or f.endswith(".yml")) and f != schema_name:
                yaml_path = os.path.join(root, f)
                if should_exclude(yaml_path):
                    continue
                schema_path = _find_schema(yaml_path, schema_name)
                if schema_path:
                    res.append(pool.apply_async(_validate, (schema_path, yaml_path, parser, strict, False)))
                else:
                    print(f"No schema found for: {yaml_path}")

    print(f"Found {len(res)} yaml files to validate...")
    for r in res:
        sub_results = r.get(timeout=300)
        error_messages.extend([str(sub_result) for sub_result in sub_results if not sub_result.isValid()])
    pool.close()
    pool.join()
    if error_messages:
        raise ValueError("\n----\n".join(set(error_messages)))


def _router(paths, schema_name, cpus, parser, excludes=None, strict=True, verbose=False):
    EXCLUDE_REGEXES = tuple(re.compile(e) for e in excludes) if excludes else tuple()

    def should_exclude(yaml_path):
        has_match = any(pattern.search(yaml_path) for pattern in EXCLUDE_REGEXES)
        if has_match and verbose:
            print("Skipping validation for %s due to exclude pattern" % yaml_path)
        return has_match

    for path in paths:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            print(f"Validating {path}...")
        else:
            raise ValueError(f"Path does not exist: {path}")

        if os.path.isdir(abs_path):
            _validate_dir(abs_path, schema_name, cpus, parser, strict, should_exclude)
        else:
            _validate_file(abs_path, schema_name, parser, strict, should_exclude)


def main():
    def int_or_auto(num_cpu):
        if num_cpu == "auto":
            return multiprocessing.cpu_count()
        return int(num_cpu)

    parser = argparse.ArgumentParser(description="Validate yaml files.")
    parser.add_argument(
        "paths",
        metavar="PATH",
        default=["./"],
        nargs="*",
        help="Paths to validate, either directories or files. Default is the current directory.",
    )
    parser.add_argument("-s", "--schema", default="schema.yaml", help="filename of schema. Default is schema.yaml.")
    parser.add_argument(
        "-e",
        "--exclude",
        metavar="PATTERN",
        action="append",
        help="Python regex used to exclude files from validation. Any substring match of a file's absolute path will be excluded. Uses default Python3 regex. Option can be supplied multiple times.",
    )
    parser.add_argument(
        "-p",
        "--parser",
        default="pyyaml",
        help='YAML library to load files. Choices are "ruamel" or "pyyaml" (default).',
    )
    parser.add_argument(
        "-n",
        "--cpu-num",
        default=4,
        type=int_or_auto,
        help="Number of child processes to spawn for validation. Default is 4. 'auto' to use CPU count.",
    )
    parser.add_argument(
        "-x",
        "--no-strict",
        action="store_true",
        help="Disable strict mode, unexpected elements in the data will be accepted.",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="show verbose information")
    parser.add_argument("-V", "--version", action="version", version=__version__)
    args = parser.parse_args()
    try:
        _router(
            paths=args.paths,
            schema_name=args.schema,
            cpus=args.cpu_num,
            parser=args.parser,
            excludes=args.exclude,
            strict=not args.no_strict,
            verbose=args.verbose,
        )
    except (SyntaxError, NameError, TypeError, ValueError) as e:
        print("Validation failed!\n%s" % str(e))
        exit(1)
    try:
        print("Validation success! 👍")
    except UnicodeEncodeError:
        print("Validation success!")


if __name__ == "__main__":
    main()
