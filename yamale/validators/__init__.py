from .base import Validator
from .validators import *

DefaultValidators = {}
def add_default_validator(validator):
    # Allow validator nodes to contain either tags or actual name
    DefaultValidators[validator.tag] = validator
    DefaultValidators[validator.__name__] = validator

for v in Validator.__subclasses__():
    add_default_validator(v)
