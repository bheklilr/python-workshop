
class Expression:
    pass


class Calculator:
    def __init__(self) -> None:
        pass

    def parse(self, expression: str) -> Expression:
        pass

    def evaluate(self, expr: Expression) -> float:
        pass

    def calculate(self, expression: str) -> float:
        expr = self.parse(expression)
        return self.evaluate(expr)
