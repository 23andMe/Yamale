import sys

PY2 = sys.version_info[0] == 2


class Result(object):
    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        error_str = '\n'.join(self.errors)
        if PY2:
            error_str = error_str.encode('utf-8')
        return error_str

    def isValid(self):
        return len(self.errors) == 0


class ValidationResult(Result):
    def __init__(self, data, schema, errors):
        super(ValidationResult, self).__init__(errors)
        self.data = data
        self.schema = schema

    def __str__(self):
        if self.isValid():
            error_str = "'%s' is Valid" % self.data
        else: 
            head_line = "Error validating data '%s' with '%s'\n\t" % (self.data, self.schema)
            error_str = head_line + '\n\t'.join(self.errors)
        if PY2:
            error_str = error_str.encode('utf-8')
        return error_str
