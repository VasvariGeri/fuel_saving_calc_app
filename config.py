import tkinter as tk
from tkinter import simpledialog, messagebox


class ConfigHelper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.YEAR = 0
        self.MONTH = 0
        self.display_gui()

    def _is_valid_year(self, year):
        year_str = str(year)
        return len(year_str) == 4 and year_str.isdigit()

    def _is_valid_month(self, month):
        month_str = str(month)
        return (len(month_str) == 1 or len(month_str) == 2) and month_str.isdigit()

    def get_year(self):
        while True:
            try:
                year = int(simpledialog.askstring("Input", "Enter year:"))
                if self._is_valid_year(year):
                    break
                else:
                    messagebox.showerror("Error", "Invalid input. Please enter a valid 4 digit year.")
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a valid 4 digit year.")
        self.YEAR = year


    def get_month(self):
        while True:
            try:
                month = int(simpledialog.askstring("Input", "Enter month:"))
                if self._is_valid_month(month):
                    break
                else:
                    messagebox.showerror("Error", "Invalid input. Please enter a valid month.")
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a valid month.")
        self.MONTH = month


    def display_gui(self):
        self.get_year()
        self.get_month()
        self.root.destroy()
