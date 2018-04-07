"""Provides the `Calculator` class for performing expression evaluation.
"""
# This ast (Abstract Syntax Tree) module is used here to do the parsing of the
# expressions.  This module can be used more generally to parse Python code into
# an object that can be worked with inside python itself, but we're mostly
# interested because it makes the process of parsing equations very easy.
# This module comes built-in to Python.
import ast


class Calculator:
    """A simple expression evaluator.  Use the `calculate` method to evaluate an
    expression into a number.
    """

    #: These are the operators that this class supports. Right now it is not
    #: used internally, but could eventually be used to make it easier to add
    # new operators to this class.
    SUPPORTED_OPERATORS = ('+', '-', '*', '/')

    def __init__(self) -> None:
        """Currently no initialization logic is needed. Can you think of what
        you might want to put here? What types of configuration could a
        calculator use?

        Some ideas:

        * Work with different bases of numbers.  A base 16 calculator would be
          useful to programmers.
        * Use Reverse Polish Notation (RPN) to parse and evaluate the equations.
        * You could store the history of the calculator and set the maximum
          number of items to keep in the history.
        """

    def parse(self, expression: str) -> ast.Expr:
        """Converts the text containing an expression into an `ast.Expr`"""
        module: ast.Module = ast.parse(expression)
        # This first element of any ast.parse call is always a body. We are only
        # interested in the value of that body. Play around with this in IPython
        # to understand it more.
        body: ast.Expr = module.body[0].value  # type: ignore
        return body

    def calculate(self, expression: str) -> float:
        """Parses and evalulates a string containing an equation into a number.
        """
        expr = self.parse(expression)
        reduced = self.evaluate(expr)
        return reduced

    def evaluate(self, expr: ast.AST) -> float:
        """Evaluates an `ast.Expr` into a number, if possible."""

        # If the expression is just a number, return that number
        if isinstance(expr, ast.Num):
            return expr.n

        # If the expression is a binary operator...
        if isinstance(expr, ast.BinOp):
            # Extract the left and right arguments of the operator and evaluate
            # each of those expressions as well
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)

            # If the operator is addition, add the left and right
            if type(expr.op) is ast.Add:
                return left + right

            # If the operator is subtraction, subtract the right from the left
            if type(expr.op) is ast.Sub:
                return left - right

            # If the operator is multiplication, multiply the left and right
            if type(expr.op) is ast.Mult:
                return left * right

            # If the operator is division, divide the left by right
            if type(expr.op) is ast.Div:
                return left / right

        # No other operations are supported at this point. Can you think of any
        # that would be useful to add?
        raise TypeError('Unsupported expression')
