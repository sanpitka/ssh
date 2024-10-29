from unittest import TestCase
from spreadsheet import SpreadSheet


class TestSpreadSheet(TestCase):

    def test_evaluate_valid_integer(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "1")
        self.assertEqual(1, spreadsheet.evaluate("A1"))

    def test_evaluate_invalid_integer(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "1.5")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_evaluate_valid_string(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "'Apple'")
        self.assertEqual("Apple", spreadsheet.evaluate("A1"))

    def test_evaluate_invalid_string(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "'Apple")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_evaluate_valid_string_with_equals(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "='Apple'")
        self.assertEqual("Apple", spreadsheet.evaluate("A1"))

    def test_evaluate_valid_int_with_equals(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1")
        self.assertEqual(1, spreadsheet.evaluate("A1"))

    def test_evaluate_invalid_string_with_equals(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "='Apple")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_evaluate_valid_integer_reference(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=B1")
        spreadsheet.set("B1", "42")
        self.assertEqual(42, spreadsheet.evaluate("A1"))

    def test_evaluate_invalid_integer_reference(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=B1")
        spreadsheet.set("B1", "42.5")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_evaluate_circular_reference(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=B1")
        spreadsheet.set("B1", "=A1")
        self.assertEqual("#Circular", spreadsheet.evaluate("A1"))

    def test_evaluate_valid_arithmetic_operation_with_integers(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1+3")
        self.assertEqual(4, spreadsheet.evaluate("A1"))

    def test_evaluate_invalid_arithmetic_operation_with_integers(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1+3.5")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_evaluate_invalid_arithmetic_operation_with_integers_2(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1/0")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_evaluate_valid_arithmetic_operation_with_integers_2(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1+3*2")
        self.assertEqual(7, spreadsheet.evaluate("A1"))

    def test_evaluate_valid_formulas_with_arithmetic_operators_and_references(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1+B1")
        spreadsheet.set("B1", "3")
        self.assertEqual(4, spreadsheet.evaluate("A1"))

    def test_evaluate_invalid_formulas_with_arithmetic_operators_and_references(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1+B1")
        spreadsheet.set("B1", "3.1")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_evaluate_invalid_arithmetic_operation_with_arithmetic_operators_2(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1+B1")
        spreadsheet.set("B1", "=A1")
        self.assertEqual("#Circular", spreadsheet.evaluate("A1"))
