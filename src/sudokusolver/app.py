"""
GUI Sudoku Solver using PySAT; formulation credit: @eysbutno
"""

import toga
from toga.style.pack import COLUMN, ROW, CENTER
import toga.validators
from .solver import solve, UNSATISFIABLE


class SudokuSolver(toga.App):
    def startup(self):
        sudoku_container = toga.Row(background_color="#565656", align_items=CENTER)
        sudoku_box = toga.Column(margin=10)
        sudoku_container.add(sudoku_box)
        for i in range(9):
            subbox = toga.Row()
            sudoku_box.add(subbox)
            for j in range(9):
                subbox.add(toga.TextInput(
                    id=f"{i}-{j}",
                    width=50,
                    height=50,
                    font_size=20,
                    margin=2,
                    validators=[
                        toga.validators.MatchRegex(r"^[1-9]$", error_message="Enter a digit from 1 to 9", allow_empty=True),
                    ]
                ))
                if j % 3 == 2 and j != 8:
                    subbox.add(toga.Box(width=15, flex=1))

            if i % 3 == 2 and i != 8:
                sudoku_box.add(toga.Box(height=15, flex=1))

        main_box = toga.Column(align_items=CENTER, gap=20, margin=20)
        main_box.add(sudoku_container)
        
        button_box = toga.Column(align_items=CENTER, gap=10)
        main_box.add(button_box)
        solve_button = toga.Button("Solve", on_press=self.solve)
        clear_button = toga.Button("Clear", on_press=self.clear)
        import_button = toga.Button("Import", on_press=self.import_data)
        self.import_input = toga.MultilineTextInput(placeholder="One per line `r c v`, 0-index", width=300, font_family="monospace")
        button_box.add(solve_button)
        button_box.add(clear_button)
        button_box.add(import_button)
        button_box.add(self.import_input)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
    
    def import_data(self, widget):
        rows = self.import_input.value.split('\n')
        for row in rows:
            try:
                data = tuple(map(int, row.split()))
            except TypeError:
                data = []
            if len(data) != 3 or data[0] >= 9 or data[0] < 0 or data[1] >= 9 or data[0] < 0:
                self.main_window.info_dialog("Error importing", "Cannot import data: Malformed data, ", data)
                return
            
            self.main_window.widgets[f"{data[0]}-{data[1]}"].value = str(data[2])

    def solve(self, widget):
        clues = []
        for i in range(9):
            for j in range(9):
                widget = self.main_window.widgets[f"{i}-{j}"]
                if widget.is_valid and widget.value:
                    clues.append((i + 1, j + 1, int(widget.value)))

        solution = solve(clues)
        if solution is UNSATISFIABLE:
            self.main_window.info_dialog("No solution", "The given clues are unsolvable.")
            return
        
        for r1 in range(9):
            for c1 in range(9):
                self.main_window.widgets[f"{r1}-{c1}"].value = str(solution[r1][c1])

    def clear(self, widget):
        for i in range(9):
            for j in range(9):
                self.main_window.widgets[f"{i}-{j}"].value = ""

def main():
    return SudokuSolver()
