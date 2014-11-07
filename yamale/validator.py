import glob
import os
from unittest import TestCase

import yamale


class YamaleTestCase(TestCase):
    schema = None
    yaml = None
    base_dir = None

    def validate(self, exception=None):
        schema = self.schema
        yaml = self.yaml
        base_dir = self.base_dir

        if schema is None:
            return

        if type(yaml) != list:
            yaml = [yaml]

        if base_dir is not None:
            schema = os.path.join(base_dir, schema)
            yaml = [os.path.join(base_dir, y) for y in yaml]

        yamale_schema = yamale.make_schema(schema)
        datas = self.create_data(yaml)

        if exception is None:
            self.assertIsNotNone(yamale.validate(yamale_schema, datas))
        else:
            self.assertRaises(exception, yamale.validate, yamale_schema, datas)

    def create_data(self, yamls):
        paths = set()
        for g in yamls:
            paths = paths.union(set(glob.glob(g)))

        data = []
        for d in [yamale.make_data(path) for path in paths]:
            for c in d:
                data.append(c)

        return data
