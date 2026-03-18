from typing import List, Optional


class Result(object):
    def __init__(self, errors: List[str]) -> None:
        self.errors = errors

    def __str__(self) -> str:
        return "\n".join(self.errors)

    def isValid(self) -> bool:
        return len(self.errors) == 0


class ValidationResult(Result):
    def __init__(self, data: Optional[str], schema: str, errors: List[str]) -> None:
        super(ValidationResult, self).__init__(errors)
        self.data = data
        self.schema = schema

    def __str__(self) -> str:
        if self.isValid():
            error_str = "'%s' is Valid" % self.data
        else:
            head_line_bits = ["Error validating data"]
            if self.data:
                head_line_bits.append("'{}'".format(self.data))
            if self.schema:
                head_line_bits.append("with schema '{}'".format(self.schema))
            head_line = " ".join(head_line_bits)
            head_line += "\n\t"
            error_str = head_line + "\n\t".join(self.errors)
        return error_str
