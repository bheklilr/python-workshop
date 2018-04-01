from typing import Dict, Callable
import tkinter as tk
from .calculator import Calculator  # noqa


# An EventHandler is a callable that takes no arguments are returns None
EventHandler = Callable[[], None]


class PyCalcUI(tk.Frame):
    def __init__(self, calculator: Calculator, parent: tk.Tk=None) -> None:
        super().__init__(parent)

        self.calculator = calculator

        self.pack()
        self.create_widgets()

    @classmethod
    def run_app(cls, calculator: Calculator, parent: tk.Tk=None) -> None:
        if parent is None:
            parent = tk.Tk()
        app = cls(calculator=calculator, parent=parent)
        app.mainloop()

    def create_widgets(self) -> None:
        self.entry_var = tk.StringVar(self, value='0')
        self.entry = tk.Entry(self, textvariable=self.entry_var)
        self.entry['justify'] = tk.RIGHT
        self.entry.grid(row=0, column=0, columnspan=4)

        opts = {
            'sticky': tk.N + tk.S + tk.E + tk.W,
            'padx': 2,
            'pady': 2,
        }
        self.btns: Dict[int, tk.Button] = {}
        for i in range(3):
            for j in range(3):
                number = 3 * i + j + 1
                row = 3 - i
                self.btns[number] = tk.Button(
                    self,
                    text=str(number),
                    command=self.on_number_clicked(number),
                )
                self.btns[number].grid(row=row, column=j, **opts)
        self.btns[0] = tk.Button(self, text='0')
        self.btns[0].grid(row=4, column=0, columnspan=2, **opts)

        self.op_btns: Dict[str, tk.Button] = {}

        self.op_btns['='] = tk.Button(self, text='=',
                                      command=self.on_eq_clicked)
        self.op_btns['='].grid(row=4, column=2, **opts)

        for i, op in enumerate(Calculator.SUPPORTED_OPERATORS, 1):
            self.op_btns[op] = tk.Button(self, text=op,
                                         command=self.on_op_clicked(op))
            self.op_btns[op].grid(row=i, column=3, **opts)

    def on_number_clicked(self, number: int) -> EventHandler:
        def on_clicked() -> None:
            current = self.entry_var.get()
            if current == '0':
                current = ''
            self.entry_var.set(current + str(number))

        return on_clicked

    def on_op_clicked(self, op: str) -> EventHandler:
        def on_clicked() -> None:
            current = self.entry_var.get()
            if current == '':
                return
            if current.endswith(op):
                return
            if not current[-1].isdigit():
                return

            if current[-1].isdigit():
                self.entry_var.set(current + op)

        return on_clicked

    def on_eq_clicked(self) -> None:
        expression = self.entry_var.get()
        try:
            result = self.calculator.calculate(expression)
        except SyntaxError:
            print(f'Expression is not valid: "{expression}"')
        else:
            self.entry_var.set(result)
