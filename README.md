Yamale (ya·ma·lē)
=================
![Hot Yamale](https://raw.githubusercontent.com/23andMe/Yamale/master/yamale.png)

A schema and validator for YAML.

What's YAML? See the current spec [here](http://www.yaml.org/spec/1.2/spec.html) and an introduction to the syntax [here] (https://github.com/Animosity/CraftIRC/wiki/Complete-idiot's-introduction-to-yaml).

[![Build Status](https://travis-ci.org/23andMe/Yamale.svg?branch=master)](https://travis-ci.org/23andMe/Yamale)
[![PyPI](https://img.shields.io/pypi/v/yamale.svg)](https://pypi.python.org/pypi/yamale)

Requirements
------------
* Python 2.7+
* Python 3.4+ (Only tested on 3.4, may work on older versions)

Install
-------
### pip
```bash
$ pip install yamale
```

### Manual
1. Download Yamale from: https://github.com/23andMe/Yamale/archive/master.zip
2. Unzip somewhere temporary
3. Run `python setup.py install` (may have to prepend `sudo`)

Usage
-----
### Command line
Yamale can be run from the command line to validate one or many YAML files. Yamale will search the directory you supply (current directory is default) for YAML files.
Each YAML file it finds it will look in the same directory as that file for its schema, if there is no schema Yamale will keep looking up the directory tree until it finds one.
If Yamale can not find a schema it will tell you.

Usage:

```bash
usage: yamale [-h] [-s SCHEMA] [-n CPU_NUM] [PATH]

Validate yaml files.

positional arguments:
  PATH                  folder to validate. Default is current directory.

optional arguments:
  -h, --help            show this help message and exit
  -s SCHEMA, --schema SCHEMA
                        filename of schema. Default is schema.yaml.
  -n CPU_NUM, --cpu-num CPU_NUM
                        number of CPUs to use. Default is 4.
```

### API
There are several ways to feed Yamale schema and data files. The simplest way is to let Yamale take care of reading and parsing your YAML files.

All you need to do is supply the files' path:
```python
# Import Yamale and make a schema object:
import yamale
schema = yamale.make_schema('./schema.yaml')

# Create a Data object
data = yamale.make_data('./data.yaml')

# Validate data against the schema. Throws a ValueError if data is invalid.
yamale.validate(schema, data)
```

If `data` is valid, nothing will happen. However, if `data` is invalid Yamale will throw a `ValueError` with a message containing all the invalid nodes.

### Schema
To use Yamale you must make a schema. A schema is a valid YAML file with one or more documents inside. Each node terminates in a string which contains valid Yamale syntax. For example, `str()` represents a [String validator](#validators).

A basic schema:
```yaml
name: str()
age: int(max=200)
height: num()
awesome: bool()
```

And some YAML that validates:
```yaml
name: Bill
age: 26
height: 6.2
awesome: True
```

Take a look at the [Examples](#examples) section for more complex schema ideas.

#### Includes
Schema files may contain more than one YAML document (nodes separated by `---`). The first document found will be the base schema. Any additional documents will be treated as Includes. Includes allow you to define a valid structure once and use it several times. They also allow you to do recursion.

A schema with an Include validator:
```yaml
person1: include('person')
person2: include('person')
---
person:
    name: str()
    age: int()
```

Some valid YAML:
```yaml
person1:
    name: Bill
    age: 70

person2:
    name: Jill
    age: 20
```

Every root node not in the first YAML document will be treated like an include:
```yaml
person: include('friend')
group: include('family')
---
friend:
    name: str()
family:
    name: str()
```

Is equivalent to:
```yaml
person: include('friend')
group: include('family')
---
friend:
    name: str()
---
family:
    name: str()
```

##### Recursion
You can get recursion using the Include validator.

This schema:
```yaml
person: include('human')
---
human:
    name: str()
    age: int()
    friend: include('human', required=False)
```

Will validate this data:
```yaml
person:
    name: Bill
    age: 50
    friend:
        name: Jill
        age: 20
        friend:
            name: Will
            age: 10
```

##### Adding external includes
After you construct a schema you can add extra, external include definitions by calling `schema.add_include(dict)`. This method takes a dictionary and adds each key as another include.

Validators
----------
Here are all the validators Yamale knows about. Every validator takes a `required` keyword telling Yamale whether or not that node must exist. By default every node is required. Example: `str(required=False)`

Some validators take keywords and some take arguments, some take both. For instance the `enum()` validator takes one or more constants as arguments and the `required` keyword: `enum('a string', 1, False, required=False)`

### String - `str(min=int, max=int, exclude=string)`
Validates strings.
- keywords
    - `min`: len(string) >= min
    - `max`: len(string) <= max
    - `exclude`: Rejects strings that contains any character in the excluded value.

Examples:
- `str(max=10, exclude='?!')`: Allows only strings less than 10 characters that don't contain `?` or `!`.

### Integer - `int(min=int, max=int)`
Validates integers.
- keywords
    - `min`: int >= min
    - `max`: int <= max

### Number - `num(min=float, max=float)`
Validates integers and floats.
- keywords
    - `min`: num >= min
    - `max`: num <= max

### Boolean - `bool()`
Validates booleans.

### Null - `null()`
Validates null values.

### Enum - `enum([primitives])`
Validates from a list of constants.
- arguments: constants to test equality with

Examples:
- `enum('a string', 1, False)`: a value can be either `'a string'`, `1` or `False`

### Day - `day(min=date, max=date)`
Validates a date in the form of YYYY-MM-DD.
- keywords
    - `min`: date >= min
    - `max`: date <= max

Examples:
- `day(min='2001-01-01', max='2100-01-01')`: Only allows dates between 2001-01-01 and 2100-01-01.

### Timestamp - `timestamp(min=time, max=time)`
Validates a timestamp in the form of YYYY-MM-DD HH:MM:SS.
- keywords
    - `min`: time >= min
    - `max`: time <= max

Examples:
- `timestamp(min='2001-01-01 01:00:00', max='2100-01-01 23:00:00')`: Only allows times between 2001-01-01 01:00:00 and 2100-01-01 23:00:00.

### List - `list([validators])`
Validates lists. If one or more validators are passed to `list()` only nodes that pass at least one of those validators will be accepted.
- arguments: one or more validators to test values with

- keywords
    - `min`: len(list) >= min
    - `max`: len(list) <= max

Examples:
- `list()`: Validates any list
- `list(include('custom'), int(), min=4)`: Only validates lists that contain the `custom` include or integers and contains a minimum of 4 items.

### Map - `map([validators])`
Validates maps. Use when you want a node to contain freeform data. Similar to `List`, `Map` also takes a number of validators to
run against its children nodes. A child validates if at least one validator passes.

Examples:
- `map()`: Validates any map
- `map(str(), int())`: Only validates maps whose children are strings or integers.

### Any - `any([validators])`
Validates against a union of types. Use when a node can contain one of several types. It is valid if at least one of the listed validators is valid.
- arguments: one or more validators to test values with

Examples:
- `any(int(), null())`: Validates an integer or a null value.
- `any(num(), include('vector'))`: Validates a number or an included 'vector' type.

### Include - `include(include_name)`
Validates included structures. Must supply the name of a valid include.
- arguments: single name of a defined include, surrounded by quotes.

Examples:
- `include('person')`

### Custom validators
It is also possible to add your own custom validators. This is an advanced topic, but here is an example of adding a `Date` validator and using it in a schema as `date()`

```python
import yamale
from yamale.validators import DefaultValidators, Validator

class Date(Validator):
    """ Custom Date validator """
    tag = 'date'

    def _is_valid(self, value):
        return isinstance(value, datetime.date)

validators = DefaultValidators.copy()  # This is a dictionary
validators[Date.tag] = Date
schema = yamale.make_schema('./schema.yaml' validators=validators)
# Then use `schema` as normal
```

Examples
--------
### Using keywords
#### Schema:
```yaml
optional: str(required=False)
optional_min: int(min=1, required=False)
min: num(min=1.5)
max: int(max=100)
```
#### Valid Data:
```yaml
optional_min: 10
min: 1.6
max: 100
```

### Includes and recursion
#### Schema:
```yaml
customerA: include('customer')
customerB: include('customer')
recursion: include('recurse')
---
customer:
    name: str()
    age: int()
    custom: include('custom_type')

custom_type:
    integer: int()

recurse:
    level: int()
    again: include('recurse', required=False)
```
#### Valid Data:
```yaml
customerA:
    name: bob
    age: 900
    custom:
        integer: 1
customerB:
    name: jill
    age: 1
    custom:
        integer: 3
recursion:
    level: 1
    again:
        level: 2
        again:
            level: 3
            again:
                level: 4
```

### Lists
#### Schema:
```yaml
list_with_two_types: list(str(), include('variant'))
questions: list(include('question'))
---
variant:
  rsid: str()
  name: str()

question:
  choices: list(include('choices'))
  questions: list(include('question'), required=False)

choices:
  id: str()
```
#### Valid Data:
```yaml
list_with_two_types:
  - 'some'
  - rsid: 'rs123'
    name: 'some SNP'
  - 'thing'
  - rsid: 'rs312'
    name: 'another SNP'
questions:
  - choices:
      - id: 'id_str'
      - id: 'id_str1'
    questions:
      - choices:
        - id: 'id_str'
        - id: 'id_str1'
```

Writing Tests
-------------
To validate YAML files when you run your program's tests use Yamale's YamaleTestCase

Example:

```python
class TestYaml(YamaleTestCase):
    base_dir = os.path.dirname(os.path.realpath(__file__))
    schema = 'schema.yaml'
    yaml = 'data.yaml'
    # or yaml = ['data-*.yaml', 'some_data.yaml']

    def runTest(self):
        self.assertTrue(self.validate())
```

`base_dir`: String path to prepend to all other paths. This is optional.

`schema`: String of path to the schema file to use. One schema file per test case.

`yaml`: String or list of yaml files to validate. Accepts globs.


Developers
----------
### Testing
Yamale uses [Tox](https://tox.readthedocs.org/en/latest/) to run its tests against multiple Python versions. To run tests, first checkout Yamale, install Tox, then run `make test` in the Yamale's root directory. You may also have to install the correct Python versions to test with as well.

### Releasing
Yamale uses Travis to upload new tags to PyPi.
To release a new version:

1. Make a commit with the new version in `setup.py`.
2. Run `make test`.
3. Push to `master`.
4. Run `make release`.

Travis will take care of the rest.
