# Need to convert from string to date using strptime
# 1. ensure that constraint is a string, not date obj
# 2. default to YYYY-MM-DD
# 3. error handling if not acceptable strptime format

from datetime import datetime

x = "12/12/2985"

datetime.strptime(x, "%m/%d/%Y")
datetime.strptime(x, "%m-%d-%Y")
# will throw ValueError if value doesn't match the format


# When creating a Schema, the args passed to a validator are parsed as 
# constraints. So I think I need to: 
# 1. Create new DateFormat constraint
# 2. Update Date(Validator) with con.Format
# 3. Update the Date(Validator).validate() function to : 
#   a. Convert to strptime if provided and ensure it converts successfully
#   b. Test if type() is datetime.date
#   c. Process rest of constraints


import yamale
from datetime import datetime
from yamale.validators import DefaultValidators, Validator


class Format(Constraint):
    keywords = {'dateformat': str}
    fail = 'Date format of %s is not %s'

    def _is_valid(self, value):
        try:
            datetime.strptime(value, self.dateformat)
        except ValueError:
            return False
        return True

    def _fail(self, value):
        return self.fail % (value, self.dateformat)


### find constraint by type in validator._constraint_inst and eval Format first



class NewDate(Validator):
    """Day validator. Format: YYYY-MM-DD"""
    value_type = date
    tag = 'day'
    constraints = [con.Min, con.Max, con.Format]

    def _is_valid(self, value):
        # Test if matches strptime format
        format_const = next((x for x in self._constraints_inst if type(x) == yamale.validators.constraints.Format), None)
        
        if format_const: 
            return isinstance(datetime.strptime(value(format_const.__dict__['format'])), date)
        else: 
            return isinstance(value, date)

    def validate(self, value):
        """
        Check if ``value`` is valid.

        :returns: [errors] If ``value`` is invalid, otherwise [].
        """
        errors = []

        # Make sure the type validates first.
        valid = self._is_valid(value)
        if not valid:
            errors.append(self.fail(value))
            return errors

        # Then validate all the constraints second.
        for constraint in self._constraints_inst:
            error = constraint.is_valid(value)
            if error:
                if isinstance(error, list):
                    errors.extend(error)
                else:
                    errors.append(error)

        return errors





validators = DefaultValidators.copy()  # This is a dictionary
validators[Date.tag] = Date
schema = yamale.make_schema('./schema.yaml', validators=validators)
# Then use `schema` as normal





######
# So it looks like if data is passed as YYYY-MM-DD then it 
# will be parsed automatically as a date by pyyaml or the other
# parser. This creates a problem because strptime requires str, 
# not datetime obj. So if users are using default then strptime
# will error. 

# Basically need to do this: 
# if not date: 
#     try: 
#       strptime
#     except: 
#       return error
# validate everything else




######################
#
# Ok current iteration seems to work (with one test) but 
# it's not the most eligant - it will eval strptime twice. 
# Once on the _is_valid() function of the validator and 
# once when looping through the individual constraints. 
# Not ideal but also not a significant issue...