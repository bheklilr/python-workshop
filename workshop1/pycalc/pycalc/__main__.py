from .ui import PyCalcUI
from .calculator import Calculator


def main() -> None:
    calculator = Calculator()
    PyCalcUI.run_app(calculator)


if __name__ == '__main__':
    main()
