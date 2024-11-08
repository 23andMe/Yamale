import os, pytest
from yamale import YamaleError
import yamale.yamale_testcase as tc

data_folder = os.path.dirname(os.path.realpath(__file__))


def test_keyed_subset_with_include_should_fail_with_correct_message():
    base_dir = data_folder
    schema = "keyed_fixtures/schema_keyed_subset_with_include.yaml"
    yaml = "keyed_fixtures/data_keyed_subset_with_include_bad.yaml"
    valid_msg = "workloads.replicas: Unexpected element"
    invalid_msg = "workloads.type: 'api' not in ('ui',)"
    
    
    with pytest.raises(YamaleError) as excinfo:
        tc.run_validate(schema, yaml, base_dir)
   
    assert valid_msg in str(excinfo.value)
    assert invalid_msg not in str(excinfo.value)


def test_keyed_subset_with_include_should_succeed():
    base_dir = data_folder
    schema = "keyed_fixtures/schema_keyed_subset_with_include.yaml"
    yaml = "keyed_fixtures/data_keyed_subset_with_include_good.yaml"

    result = tc.run_validate(schema, yaml, base_dir)
    assert result == True


def test_keyed_any_with_include_should_fail_with_correct_message():
    base_dir = data_folder
    schema = "keyed_fixtures/schema_keyed_any_with_include.yaml"
    yaml = "keyed_fixtures/data_keyed_any_with_include_bad.yaml"
    valid_msg = "deploy.branch: Unexpected element"
    invalid_msg = "deploy.strategy: 'branch' not in ('preview',)"

    with pytest.raises(YamaleError) as excinfo:
        tc.run_validate(schema, yaml, base_dir)
    
    assert valid_msg in str(excinfo.value)
    assert invalid_msg not in str(excinfo.value)


def test_keyed_any_with_include_should_succeed():
    base_dir = data_folder
    schema = "keyed_fixtures/schema_keyed_any_with_include.yaml"
    yaml = "keyed_fixtures/data_keyed_any_with_include_good.yaml"
    result = tc.run_validate(schema, yaml, base_dir)
    assert result == True
