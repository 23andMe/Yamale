Yamale (ya·ma·lē)
=================
![Hot Yamale](https://raw2.github.com/23andMe/Yamale/master/yamale.png)

A schema and validator for YAML.

[![Build Status](https://travis-ci.org/23andMe/Yamale.svg?branch=master)](https://travis-ci.org/23andMe/Yamale)

Requirements
------------
* Python 2.7+
* Python 3.4+ (Only tested on 3.4, may work on older versions)

Install
-------
1. Download Yamale from: https://github.com/23andMe/Yamale/archive/master.zip
2. Unzip somewhere temporary
3. Run `python setup.py install` (may have to prepend `sudo`)

Usage
-----
### Validating
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

Some validators take keywords and some take arguments. For instance the `enum()` validator takes one or more constants as arguments: `enum('a string', 1, False, required=False)`

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

### Enum - `enum([primitives])`
Validates from a list of constants.
- arguments: constants to test equality with

Examples:
- `enum('a string', 1, False)`: a value can be either `'a string'`, `1` or `False`

### List - `list([validators])`
Validates lists. If validators are passed to `list()` only nodes that pass at least one of those validators will be accepted.
- arguments: validators to test values with

Examples:
- `list()`: Validates any list
- `list(str(), int())`: Only validates lists that contain strings or integers.

### Map - `map([validators])`
Validates maps. Use when you want a node to contain freeform data. Similar to `List`, `Map` also takes a number of validators to
run against its children nodes. A child validates if at least one validator passes.

Examples:
- `map()`: Validates any map
- `map(str(), int())`: Only validates maps whose children are strings or integers.

### Include - `include(include_name)`
Validates included structures. Must supply the name of a valid include.
- arguments: single name of a defined include, surrounded by quotes.

Examples:
- `include('person')`

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
simple: list(str(), int())
questions: list(include('question'))
---
question:
  choices: list(include('choices'))
  questions: list(include('question'), required=False)

choices:
  id: str()
```
#### Valid Data:
```yaml
simple:
  - 'this'
  - 'is'
  - 'a'
  - 100
  - 10
questions:
  - choices:
      - id: 'id_str'
      - id: 'id_str1'
    questions:
      - choices:
        - id: 'id_str'
        - id: 'id_str1'
```
