from pytest import fixture

from pycalc.calculator import Calculator


@fixture
def calc():
    return Calculator()


def test_simple_arithmetic_add(calc):
    assert calc.calculate('2 + 2') == 4
