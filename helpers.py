import pandas as pd
from tkinter import messagebox


class FileReaderHelper:
    def __init__(self, year, month):
        self.YEAR = year
        self.MONTH = month

    def read_riport_file(self):
        try:
            mol_excel_file = pd.ExcelFile(f"./input/Ellenörző riport {self.YEAR} {self.MONTH}.xlsx")
        except FileNotFoundError:
            messagebox.showerror("Error", f"No such file: \nEllenörző riport {self.YEAR} {self.MONTH}.xlsx")
            exit(1)
        mol_riport_sheets = mol_excel_file.sheet_names
        return pd.read_excel(f"./input/Ellenörző riport {self.YEAR} {self.MONTH}.xlsx", sheet_name=mol_riport_sheets[0])

    def read_waybill_file(self, plate_nrs):
        try:
            waybill_excel_file = pd.ExcelFile(f"./input/Fuvarlevél nyilvántartás {self.YEAR}.xlsx")
        except FileNotFoundError:
            messagebox.showerror("Error", f"No such file: \nFuvarlevél nyilvántartás {self.YEAR}.xlsx")
            exit(1)
        waybill_sheets = waybill_excel_file.sheet_names
        waybills = {}
        for waybill in waybill_sheets:
            transformed_plate_nr = waybill.replace("-", "")
            if transformed_plate_nr in plate_nrs:
                waybills[transformed_plate_nr] = (pd.read_excel(f"./input/Fuvarlevél nyilvántartás {self.YEAR}.xlsx", sheet_name=waybill))
        return waybills
