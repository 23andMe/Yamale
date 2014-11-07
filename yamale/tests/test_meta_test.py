import os
from yamale import YamaleTestCase


class TestYaml(YamaleTestCase):
    base_dir = os.path.dirname(os.path.realpath(__file__))
    schema = 'fixtures/custom_types.yaml'
    yaml = 'fixtures/custom_types_good.yaml'

    def runTest(self):
        self.validate()


class TestBadYaml(YamaleTestCase):
    base_dir = os.path.dirname(os.path.realpath(__file__))
    schema = 'fixtures/custom_types.yaml'
    yaml = 'fixtures/custom_types_bad.yaml'

    def runTest(self):
        self.validate(exception=ValueError)
