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

#### Includes
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
