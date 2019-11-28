import re
import os
from yamale import YamaleTestCase
from yamale.validators import DefaultValidators, Validator


data_folder = os.path.dirname(os.path.realpath(__file__))


class TestAllYaml(YamaleTestCase):
    base_dir = data_folder
    schema = 'meta_test_fixtures/schema.yaml'
    yaml = 'meta_test_fixtures/data_custom.yaml'

    def runTest(self):
        self.assertTrue(self.validate())


class TestBadYaml(YamaleTestCase):
    base_dir = data_folder
    schema = 'meta_test_fixtures/schema_bad.yaml'
    yaml = 'meta_test_fixtures/data*.yaml'

    def runTest(self):
        self.assertRaises(ValueError, self.validate)


class TestMapYaml(YamaleTestCase):
    base_dir = data_folder
    schema = 'meta_test_fixtures/schema.yaml'
    yaml = ['meta_test_fixtures/data_custom.yaml',
            'meta_test_fixtures/some_data.yaml',
            # Make sure  schema doesn't validate itself
            'meta_test_fixtures/schema.yaml']

    def runTest(self):
        self.assertTrue(self.validate())


# class TestListYaml(YamaleTestCase):
#     base_dir = data_folder
#     schema = 'meta_test_fixtures/schema_include_list.yaml'
#     yaml = ['meta_test_fixtures/data_include_list.yaml']

#     def runTest(self):
#         self.assertTrue(self.validate())


class Card(Validator):
    """ Custom validator for testing purpose """
    tag = 'card'
    card_regex = re.compile(r'^(10|[2-9JQKA])[SHDC]$')

    def _is_valid(self, value):
        return re.match(self.card_regex, value)

class Environment(Validator):
    """ Custom validator for testing purpose """
    tag = 'environment'
    ENVIRONMENTS = ['dev','stg','prd']

    def __init__(self, *args, **kwargs):
        self.validators = [val for val in args if isinstance(val, Validator)]
        super(Environment, self).__init__(*args, **kwargs)

    def _is_valid(self, value):
        envs = value.keys()
        for env in envs:
            self.env = env
            return False if env not in self.ENVIRONMENTS else True
    
    def fail(self, value):
        return 'Environment \'%s\' not in %s' % (self.env, self.ENVIRONMENTS)

class TestCustomValidator(YamaleTestCase):
    base_dir = data_folder
    schema = 'meta_test_fixtures/schema_custom.yaml'
    yaml = 'meta_test_fixtures/data_custom.yaml'

    def runTest(self):
        validators = DefaultValidators.copy()
        validators['card'] = Card
        self.assertTrue(self.validate(validators))

class TestCustomValidatorWithIncludes(YamaleTestCase):
    base_dir = data_folder
    schema = 'meta_test_fixtures/schema_custom_with_include.yaml'
    yaml = 'meta_test_fixtures/data_custom_with_include.yaml'

    def runTest(self):
        validators = DefaultValidators.copy()
        validators[Card.tag] = Card
        self.assertTrue(self.validate(validators))

class TestCustomValidatorWithIncludesComplex(YamaleTestCase):
    base_dir = data_folder
    schema = 'meta_test_fixtures/schema_custom_with_include_complex.yaml'
    yaml = 'meta_test_fixtures/data_custom_with_include_complex.yaml'

    def runTest(self):
        validators = DefaultValidators.copy()
        validators[Environment.tag] = Environment
        validators[Card.tag] = Card
        self.assertTrue(self.validate(validators))

class TestCustomValidatorWithIncludesComplexFail(YamaleTestCase):
    base_dir = data_folder
    schema = 'meta_test_fixtures/schema_custom_with_include_complex.yaml'
    yaml = 'meta_test_fixtures/data_custom_with_include_complex_fail.yaml'

    def runTest(self):
        validators = DefaultValidators.copy()
        validators[Environment.tag] = Environment
        validators[Card.tag] = Card
        with self.assertRaises(ValueError) as cm:
            self.validate(validators)

class TestBadRequiredYaml(YamaleTestCase):
    base_dir = data_folder
    schema = 'meta_test_fixtures/schema_required_bad.yaml'
    yaml = 'meta_test_fixtures/data_required_bad.yaml'

    def runTest(self):
        self.assertRaises(ValueError, self.validate)


class TestGoodRequiredYaml(YamaleTestCase):
    base_dir = data_folder
    schema = 'meta_test_fixtures/schema_required_good.yaml'
    yaml = 'meta_test_fixtures/data_required_good.yaml'

    def runTest(self):
        self.assertTrue(self.validate())
