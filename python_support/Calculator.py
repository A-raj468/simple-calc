import re

op_allows = ["+", "-", "*", "/", "%"]


class Calculator:
    def __init__(self) -> None:
        self.expr = ""
        self.rpn = []
        self.value = 0

    def evaluate(self, expr: str) -> int:
        self.expr = expr
        self.rpn = self._rpn()
        self.value = self._eval()
        return self.value

    def get_value(self) -> int:
        return self.value

    def get_rpn(self) -> list:
        return self.rpn

    def _rpn(self) -> list:
        def tokenize(expr: str) -> list[str]:
            expr = re.sub(r"^\s*-", r"0-", expr)
            expr = re.sub(r"\(\s*-", r"(0-", expr)

            pattern = re.compile(
                r"\d+|" + "|".join([rf"\{op}" for op in op_allows] + [r"\(", r"\)"])
            )
            tokens = re.findall(pattern, expr)
            return tokens

        def precedence(operator: str) -> int:
            if operator in ["+", "-"]:
                return 1
            elif operator in ["*", "/", "%"]:
                return 2
            elif operator in ["(", ")"]:
                return 0
            else:
                return -1

        rpn = []

        operators = []

        for token in tokenize(self.expr):
            if token in ["+", "-", "*", "/", "%"]:
                while len(operators) > 0 and precedence(operators[-1]) >= precedence(
                    token
                ):
                    rpn.append(operators.pop())
                operators.append(token)

            elif token == "(":
                operators.append(token)

            elif token == ")":
                while operators[-1] != "(":
                    rpn.append(operators.pop())
                operators.pop()

            else:
                rpn.append(int(token))

        while len(operators) > 0:
            rpn.append(operators.pop())

        return rpn

    def _eval(self) -> int:
        value_stack = []

        for ops in self.rpn:
            if ops in ["+", "-", "*", "/", "%"]:
                val2 = value_stack.pop()
                val1 = value_stack.pop()
                if ops == "+":
                    value_stack.append(val1 + val2)
                elif ops == "-":
                    value_stack.append(val1 - val2)
                elif ops == "*":
                    value_stack.append(val1 * val2)
                elif ops == "/":
                    value_stack.append(val1 // val2)
                elif ops == "%":
                    value_stack.append(val1 % val2)

            else:
                value_stack.append(ops)

        if len(value_stack) == 1:
            return value_stack[0]

        return -1

    def __str__(self) -> str:
        return f"Expr: {self.expr}\nRPN: {self.rpn}\nValue: {self.value}"


if __name__ == "__main__":
    calc = Calculator()
    expr = "-3 + 4 * 2"
    calc.evaluate(expr)
    print(calc)
