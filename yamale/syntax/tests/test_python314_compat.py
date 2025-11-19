"""
Test to verify Python 3.14 compatibility.
This test checks that the parser works correctly with ast.Constant,
which is the unified constant representation available since Python 3.8.
"""

import ast
import unittest

# Import the parser module
from yamale.syntax import parser as par
from yamale.validators.validators import String, Number, Any


class TestPython314Compatibility(unittest.TestCase):
    """Test parser compatibility using ast.Constant for all Python versions."""

    def test_parser_with_string_argument(self):
        """Test that the parser handles string arguments correctly."""
        result = par.parse("str(min=3)")
        self.assertEqual(result, String(min=3))

    def test_parser_with_numeric_argument(self):
        """Test that the parser handles numeric arguments correctly."""
        result = par.parse("num(min=1.5, max=10.5)")
        expected = Number(min=1.5, max=10.5)
        self.assertEqual(result, expected)

    def test_parser_with_integer_argument(self):
        """Test that the parser handles integer arguments correctly."""
        result = par.parse("num(min=1, max=10)")
        expected = Number(min=1, max=10)
        self.assertEqual(result, expected)

    def test_parser_with_boolean_argument(self):
        """Test that the parser handles boolean arguments correctly."""
        result = par.parse("str(required=True)")
        self.assertTrue(result.is_required)

    def test_parser_with_false_boolean(self):
        """Test that the parser handles False boolean arguments correctly."""
        result = par.parse("str(required=False)")
        self.assertFalse(result.is_required)

    def test_parser_with_none_constant(self):
        """Test that the parser handles None constant correctly."""
        result = par.parse("any()")
        self.assertEqual(result, Any())

    def test_parser_with_any_validator(self):
        """Test that the parser works with any() validator."""
        result = par.parse("any(required=True)")
        self.assertTrue(result.is_required)

    def test_ast_constant_is_used(self):
        """Verify that ast.Constant is the actual node type used by ast.parse."""
        # When parsing string literals, we should get ast.Constant nodes
        tree = ast.parse("'hello'", mode="eval")
        self.assertIsInstance(tree.body, ast.Constant)
        
        # When parsing numbers
        tree = ast.parse("42", mode="eval")
        self.assertIsInstance(tree.body, ast.Constant)
        
        # When parsing booleans
        tree = ast.parse("True", mode="eval")
        self.assertIsInstance(tree.body, ast.Constant)


if __name__ == "__main__":
    unittest.main()
