import unittest

from Calculator import Calculator

calc = Calculator()


# Test case class
class TestRPN(unittest.TestCase):
    def test_simple_expression(self):
        infix_expr = "-3 + 4 * 2"
        expected_rpn = [0, 3, "-", 4, 2, "*", "+"]
        calc.evaluate(infix_expr)
        actual_rpn = calc.get_rpn()
        self.assertEqual(actual_rpn, expected_rpn)

    def test_expression_with_parentheses(self):
        infix_expr = "3 * (-4 + 2)"
        expected_rpn = [3, 0, 4, "-", 2, "+", "*"]
        calc.evaluate(infix_expr)
        actual_rpn = calc.get_rpn()
        self.assertEqual(actual_rpn, expected_rpn)

    def test_expression_with_different_precedence(self):
        infix_expr = "3 + 4 * 2 / (1 - 5) % 2"
        expected_rpn = [3, 4, 2, "*", 1, 5, "-", "/", 2, "%", "+"]
        calc.evaluate(infix_expr)
        actual_rpn = calc.get_rpn()
        self.assertEqual(actual_rpn, expected_rpn)


class TestEvaluateRPN(unittest.TestCase):

    def test_simple_expression(self):
        infix_expr = "-3 + 4 * 2"
        expected_result = 5
        actual_result = calc.evaluate(infix_expr)
        self.assertEqual(actual_result, expected_result)

    def test_expression_with_parentheses(self):
        infix_expr = "3 * (-4 + 2)"
        expected_result = -6
        actual_result = calc.evaluate(infix_expr)
        self.assertEqual(actual_result, expected_result)

    def test_expression_with_different_precedence(self):
        infix_expr = "3 + 4 * 2 / (1 - 5) % 2"
        expected_result = 3
        actual_result = calc.evaluate(infix_expr)
        self.assertEqual(actual_result, expected_result)


# Running the tests
if __name__ == "__main__":
    unittest.main()
