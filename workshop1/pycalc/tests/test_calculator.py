from pytest import fixture

from pycalc.calculator import Calculator


@fixture
def calc():
    return Calculator()


def test_simple_arithmetic_add(calc):
    assert calc.calculate('2 + 2') == 4


def test_simple_arithmetic_subtract(calc):
    assert calc.calculate('2 - 1') == 1


def test_simple_arithmetic_multiply(calc):
    assert calc.calculate('3 * 4') == 12


def test_simple_arithmetic_divide(calc):
    assert calc.calculate('10 / 3') == (10 / 3)
