import tkinter as tk
from tkinter import simpledialog, messagebox

class ConfigHelper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.YEAR = 0
        self.MONTH = 0

    def _get_input(self, prompt, validator):
        dialog_window = tk.Toplevel(self.root)
        dialog_window.withdraw()
        while True:
            try:
                user_input = int(simpledialog.askstring("Input", prompt))
                if validator(user_input):
                    return user_input
                else:
                    messagebox.showerror("Error", f"Invalid input. Please enter a valid {prompt}.")
            except ValueError:
                messagebox.showerror("Error", f"Invalid input. Please enter a valid {prompt}.")

    def _is_valid_year(self, year):
        return 1980 <= year <= 2200

    def _is_valid_month(self, month):
        return 1 <= month <= 12

    def _get_year(self):
        self.YEAR = self._get_input("Enter year:", self._is_valid_year)

    def _get_month(self):
        self.MONTH = self._get_input("Enter month:", self._is_valid_month)

    def display_gui(self):
        self._get_year()
        self._get_month()
        self.root.destroy()
