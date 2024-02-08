import pandas as pd
import yaml
from tkinter import messagebox


class FileReaderHelper:
    def __init__(self, year, month):
        self.YEAR = year
        self.MONTH = month

    def read_riport_file(self):
        riport_filepath = f"./input/Ellenörző riport {self.YEAR} {self.MONTH}.xlsx"
        try:
            mol_excel_file = pd.ExcelFile(riport_filepath)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No such file: \n{riport_filepath}")
            exit(1)
        mol_riport_sheets = mol_excel_file.sheet_names
        return pd.read_excel(riport_filepath, sheet_name=mol_riport_sheets[0])

    def read_waybill_file(self, plate_nrs):
        waybill_filepath = f"./input/Fuvarlevél nyilvántartás {self.YEAR}.xlsx"
        try:
            waybill_excel_file = pd.ExcelFile(waybill_filepath)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No such file: \n{waybill_filepath}")
            exit(1)
        waybill_sheets = waybill_excel_file.sheet_names
        waybills = {}
        for waybill in waybill_sheets:
            transformed_plate_nr = waybill.replace("-", "")
            if transformed_plate_nr in plate_nrs:
                waybills[transformed_plate_nr] = (pd.read_excel(waybill_filepath, sheet_name=waybill))
        return waybills

    def read_norma_file(self):
        norma_filepath = f"./input/norma_segédtáblázat.yml"
        with open(norma_filepath, 'r') as file:
            data = yaml.safe_load(file)
        print(data)
