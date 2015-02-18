import datetime
import os
from yamale import YamaleTestCase
from yamale.validators import DefaultValidators, Validator


data_folder = os.path.dirname(os.path.realpath(__file__))


class TestAllYaml(YamaleTestCase):
    base_dir = data_folder
    schema = 'meta_test_fixtures/schema.yaml'
    yaml = 'meta_test_fixtures/data*.yaml'

    def runTest(self):
        self.assertTrue(self.validate())


class TestBadYaml(YamaleTestCase):
    base_dir = data_folder
    schema = 'meta_test_fixtures/schema_bad.yaml'
    yaml = 'meta_test_fixtures/data*.yaml'

    def runTest(self):
        self.assertRaises(ValueError, self.validate)


class TestListYaml(YamaleTestCase):
    base_dir = data_folder
    schema = 'meta_test_fixtures/schema.yaml'
    yaml = ['meta_test_fixtures/data*.yaml',
            'meta_test_fixtures/some_data.yaml',
            # Make sure  schema doesn't validate itself
            'meta_test_fixtures/schema.yaml']

    def runTest(self):
        self.assertTrue(self.validate())


class Date(Validator):
    """ Custom validator for testing purpose """
    tag = 'date'

    def _is_valid(self, value):
        return isinstance(value, datetime.date)


class TestCustomValidator(YamaleTestCase):
    base_dir = data_folder
    schema = 'meta_test_fixtures/schema_custom.yaml'
    yaml = 'meta_test_fixtures/data_custom.yaml'

    def runTest(self):
        validators = DefaultValidators.copy()
        validators['date'] = Date
        self.assertTrue(self.validate(validators))
