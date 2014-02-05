Schemata
========
A schema validator for YAML.

About
-----
Schemata allows you to validate YAML files against a YAML schema.

Requirements
------------
Python 2.7

Install
-------
1. Download Schemata from: https://github.com/23andMe/Schemata/archive/master.zip
2. Unzip somewhere temporary
3. Run `python setup.py install` (may have to prepend `sudo`)

Usage
-----
### Schema
You must first make a schema to use Schemata. A schema is a valid YAML file with one or more documents inside. Each node terminates in a string which contains valid Schemata syntax. For example, `str()` represents a String validator.

A basic schema:
```yaml
name: str()
```

And some YAML that validates:
```yaml
name: Bill
```

Take a look at the Examples section for more complex schema ideas.

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
##### Recursion
### Validating

Validators
----------
### String - `str()`
### Integer - `int()`
### Number - `num()`
### Boolean - `bool()`
### Enum - `enum([primitives])`
### List - `list([validators])`
### Include - `include(include_name)`

Examples
--------
