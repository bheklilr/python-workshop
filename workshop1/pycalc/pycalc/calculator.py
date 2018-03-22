import ast


class Calculator:
    def __init__(self) -> None:
        pass

    def parse(self, expression: str) -> ast.Expr:
        module: ast.Module = ast.parse(expression)
        body: ast.Expr = module.body[0].value
        return body

    def calculate(self, expression: str) -> float:
        expr = self.parse(expression)
        reduced = self.evaluate(expr)
        return reduced

    def evaluate(self, expr: ast.AST) -> float:
        if isinstance(expr, ast.Num):
            return expr.n

        if isinstance(expr, ast.BinOp):
            if type(expr.op) is ast.Add:
                left = self.evaluate(expr.left)
                right = self.evaluate(expr.right)
                return left + right

        raise TypeError('Unsupported expression')
