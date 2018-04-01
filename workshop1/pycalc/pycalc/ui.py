import tkinter as tk
from .calculator import Calculator  # noqa


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
        self.entry = tk.Entry(self, textvariable=self.entry_var, justify=tk.RIGHT)
        self.entry.grid(row=0, column=0, columnspan=3)

        opts = {
            'sticky':tk.N + tk.S + tk.E + tk.W,
            'padx': 2,
            'pady': 2,
        }
        self.btns = {}
        for i in range(3):
            for j in range(3):
                number = 3 * i + j + 1
                self.btns[number] = tk.Button(self, text=str(number))
                self.btns[number].grid(row=i + 1, column=j, **opts)
        self.btns[0] = tk.Button(self, text='0')
        self.btns[0].grid(row=4, column=0, columnspan=2, **opts)
        self.compute_btn = tk.Button(self, text='=')
        self.compute_btn.grid(row=4, column=2, **opts)
