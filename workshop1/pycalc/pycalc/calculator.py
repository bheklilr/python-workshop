
class Expression:
    pass


class Calculator:
    def __init__(self) -> None:
        pass

    def parse(self, expression: str) -> Expression:
        pass

    def calculate(self, expression: str) -> float:
        return eval(expression)
