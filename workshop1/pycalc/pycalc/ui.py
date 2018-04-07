from typing import Dict, Callable
import tkinter as tk
from .calculator import Calculator  # noqa


# An EventHandler is a callable that takes no arguments are returns None
EventHandler = Callable[[], None]


class PyCalcUI(tk.Frame):
    def __init__(self, calculator: Calculator, parent: tk.Tk=None) -> None:
        super().__init__(parent)

        self.calculator = calculator

        # This draws the PyCalcUI in the main window
        self.pack()
        # Create the UI itself
        self.create_widgets()

    @classmethod
    def run_app(cls, calculator: Calculator, parent: tk.Tk=None) -> None:
        """Creates and runs an Application object using the given Calculator.
        """
        if parent is None:
            # If the parent is None, create a new Tk application object.
            parent = tk.Tk()
        # Create the PyCalcUI object
        app = cls(calculator=calculator, parent=parent)
        # Run it
        app.mainloop()

    def create_widgets(self) -> None:
        """Creates all of the widgets for the PyCalcUI
        """
        # In Tkinter, you connect a SomethingVar to an input for getting and
        # setting the value in the input itself. For an Entry, use a StringVar.
        self.entry_var = tk.StringVar(self, value='0')
        self.entry = tk.Entry(self, textvariable=self.entry_var)
        self.entry['justify'] = tk.RIGHT
        # Place the entry in row 0, col 0, spanning 4 columns.
        self.entry.grid(row=0, column=0, columnspan=4)

        # These are global options to use for all the buttons
        opts = {
            # Makes the edges of the button stick to the top, bottom, left, and
            # right of the container.
            'sticky': tk.N + tk.S + tk.E + tk.W,
            # Add a bit of padding
            'padx': 2,
            'pady': 2,
        }
        # We will store all the number buttons in a dictionary mapping the
        # number to the button
        self.btns: Dict[int, tk.Button] = {}
        for i in range(3):  # 0, 1, 2
            for j in range(3):  # 0, 1, 2
                # This equation will calculate 1 to 9 in order using i and j
                number = 3 * i + j + 1
                # We want to start on the 4th row (0 index) and move up a row
                # every 3 buttons
                row = 3 - i
                # Create the button, and set up the callback for when the button
                # is clicked
                self.btns[number] = tk.Button(
                    self,
                    text=str(number),
                    command=self.on_number_clicked(number),
                )
                self.btns[number].grid(row=row, column=j, **opts)
        # Manually create the 0 button since it doesn't follow the same pattern
        # as the other buttons.
        self.btns[0] = tk.Button(self, text='0',
                                 command=self.on_number_clicked(0))
        self.btns[0].grid(row=4, column=0, columnspan=2, **opts)

        # We wil store the buttons for operators in the same way
        self.op_btns: Dict[str, tk.Button] = {}

        # The equals button is special and gets its own handler
        self.op_btns['='] = tk.Button(self, text='=',
                                      command=self.on_eq_clicked)
        self.op_btns['='].grid(row=4, column=2, **opts)

        # Add the rest of the operator buttons using the supported operators
        for i, op in enumerate(self.calculator.SUPPORTED_OPERATORS, 1):
            self.op_btns[op] = tk.Button(self, text=op,
                                         command=self.on_op_clicked(op))
            self.op_btns[op].grid(row=i, column=3, **opts)

    def on_number_clicked(self, number: int) -> EventHandler:
        """Creates an EventHandler for the given number. Tkinter requires this
        because you can't find out what button was pressed from the event.
        """
        # Define a new EventHandler that handles the button click
        def on_clicked() -> None:
            current = self.entry_var.get()
            if current == '0':
                current = ''
            self.entry_var.set(current + str(number))

        # Return the EventHandler
        return on_clicked

    def on_op_clicked(self, op: str) -> EventHandler:
        """Creates an EventHandler for the given operation. Tkinter requires
        this because you can't find out what button was pressed from the event.
        """
        # Define a new EventHandler that handles the button click
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

        # Return the EventHandler
        return on_clicked

    def on_eq_clicked(self) -> None:
        """Computes the inputed expression and displays the result back.
        """
        expression = self.entry_var.get()
        try:
            result = self.calculator.calculate(expression)
        except SyntaxError:
            # Just prints out the error to the console. Consider adding a
            # message box or coloring the text red to indicate an error.
            print(f'Expression is not valid: "{expression}"')
        except TypeError:
            print(f'Unsupported operation in expression "{expression}"')
        else:
            self.entry_var.set(result)
