from tkinter import simpledialog, messagebox, Tk


class ConfigHelper:
    def __init__(self):
        self.YEAR = None
        self.MONTH = None
        self.FUEL_PRICE = None
        self.LIMIT = None
        self.root = Tk()
        self.root.withdraw()

    def _get_input(self, prompt, validator):
        while True:
            user_input = simpledialog.askinteger("Input", prompt)
            if validator(user_input):
                return user_input
            else:
                messagebox.showerror("Error", "Invalid input.\nPlease enter a valid value.\nE.g. year: 2020, month: 5,\nfuel price: 650, limit: 100000")

    def _is_valid_year(self, year):
        return 1980 <= year <= 2200 and year is not None

    def _is_valid_month(self, month):
        return 1 <= month <= 12 and month is not None

    def _is_valid_price(self, price):
        return 0 < price and price is not None

    def _is_valid_limit(self, limit):
        if limit != 100000:
            messagebox.showwarning("Warning", "Limit is not set to default 100.000")
        return 0 < limit and limit is not None

    def _get_year(self):
        self.YEAR = self._get_input("Enter year:", self._is_valid_year)

    def _get_month(self):
        self.MONTH = self._get_input("Enter month:", self._is_valid_month)

    def _get_fuel_price(self):
        self.FUEL_PRICE = self._get_input("Enter fuel price:", self._is_valid_price)

    def _get_limit(self):
        self.LIMIT = self._get_input("Enter payable limit:", self._is_valid_limit)

    def get_inputs(self):
        self._get_year()
        self._get_month()
        self._get_fuel_price()
        self._get_limit()
