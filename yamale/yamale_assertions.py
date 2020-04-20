import glob
import os
import itertools
from pytest import fail

from yamale import *

class YamaleAssertions:

    def _assert(self, yaml, schema, base_dir, expected_files, validators):
        if schema is None:
            return
        
        if type(yaml) != list:
            yaml = [yaml]
        
        if base_dir is not None:
            schema = os.path.join(base_dir, schema)
            yaml = {os.path.join(base_dir, y) for y in yaml}

        # Run yaml through glob and flatten list
        yaml = set(itertools.chain(*map(glob.glob, yaml)))

        # Remove schema from set of data files
        yaml = yaml - {schema}

        yamale_schema = yamale.make_schema(schema, validators=validators)
        yamale_data = itertools.chain(*map(yamale.make_data, yaml))

        results = yamale.validate(yamale_schema, yamale_data)
        if expected_files is not None:
            assert results == expected_files, "Not expected number of processed file"
        return results

    def assertIsValid(self, yaml, schema, base_dir=None, expected_files=None, validators=None):
        """ assert method for easily validating YAML in your own tests.
        `schema`: String of path to the schema file to use.
        `yaml`: String or list of yaml files to validate. Accepts globs.
        `base_dir`: String path to prepend to all other paths. This is optional.
        `expected_files`: Number of expected files validated. This optional.
        """
        for result in self._assert(yaml, schema, base_dir, expected_files, validators):
            assert result.isValid

    def assertError(self, yaml, schema, expected_error, base_dir=None, expected_files=None, validators=None):
        """ assert method for easily validating YAML in your own tests.
        `schema`: String of path to the schema file to use.
        `yaml`: String or list of yaml files to validate. Accepts globs.
        `expected`: String of expected error
        `base_dir`: String path to prepend to all other paths. This is optional.
        `expected_files`: Number of expected files validated. This optional.
        """
        for result in self._assert(yaml, schema, base_dir, expected_files, validators):
            if result.hasError(expected_error):
                return

        fail("Doesn't return expected error: %s" % expected_error)
