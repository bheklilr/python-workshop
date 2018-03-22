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
        pass
