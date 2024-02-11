import os
from pandas import ExcelFile, read_excel
from yaml import safe_load
from tkinter import messagebox
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.tables import TableStyle
from reportlab.lib import colors


class FileIOHelper:
    def __init__(self, year, month, fuel_price, limit):
        self.YEAR = year
        self.MONTH = month
        self.FUEL = fuel_price
        self.LIMIT = limit

    def read_riport_file(self):
        riport_filepath = f"./input/Ellenörző riport {self.YEAR} {self.MONTH}.xlsx"
        try:
            mol_excel_file = ExcelFile(riport_filepath)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No such file: \n{riport_filepath}")
            exit(1)
        mol_riport_sheets = mol_excel_file.sheet_names
        return read_excel(riport_filepath, sheet_name=mol_riport_sheets[0])

    def read_waybill_file(self):
        waybill_filepath = f"./input/Fuvarlevél nyilvántartás 2023.xlsx"
        try:
            waybill_excel_file = ExcelFile(waybill_filepath)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No such file: \n{waybill_filepath}")
            exit(1)
        waybill_sheets = waybill_excel_file.sheet_names
        waybills = {}
        for waybill in waybill_sheets:
            transformed_plate_nr = waybill.replace("-", "")
            if waybill != "Adatforrás":
                try:
                    waybills[transformed_plate_nr] = (read_excel(waybill_filepath, sheet_name=waybill))
                except ValueError:
                    messagebox.showerror("Error", f"No sheet in fuvarlevél nyilvántartás for:\n{waybill}")

        return waybills

    def read_norma_file(self):
        norma_filepath = f"./input/norma_segédtáblázat.yml"
        if not os.path.exists(norma_filepath):
            messagebox.showerror("Error", "Norma file missing")
            exit(1)
        with open(norma_filepath, 'r') as file:
            data = safe_load(file)
        return data

    def write_payroll_file(self, drivers, all_money, all_distance):
        output_dir = "./output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filepath = f"./output/Bérfizetési jegyzék {self.YEAR} {self.MONTH}.pdf"
        doc = SimpleDocTemplate(filepath)
        elements = []
        space = Spacer(1, 24)
        elements.append(space)
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=getSampleStyleSheet()['Title'],
            alignment=1
        )
        title_text = f"Üzemanyag megtakarítás {self.YEAR}.{self.MONTH}"
        title = Paragraph(title_text, style=title_style, encoding="utf-8")
        elements.append(title)
        title_space = Spacer(1, 48)
        elements.append(title_space)
        table_data = self._generate_table_data(drivers, all_money, all_distance)
        table_style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add borders to all cells
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Add background color to the header row
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Set text color for the header row
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),  # Make the first line bold
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),  # Make the last line bold
        ])
        table = Table(table_data, style=table_style)
        elements.append(table)
        elements.append(space)
        elements.append(Paragraph(f"Gázolaj egységár: {self.FUEL}"))
        doc.build(elements)


    def _generate_table_data(self, drivers, all_money, all_distance):
        table_data = [["Név", "Teljesített km", "Megtak liter", "Megtak Ft", "Kifizethető", "Átvételi elismerés"]]
        all_saved_fuel = 0
        possible_money_saved = 0
        for driver in drivers.values():
            all_saved_fuel += driver.fuel_saved
            possible_money_saved += driver.money_saved
            payable = self.LIMIT if self.LIMIT < driver.money_saved else driver.money_saved
            driver_params = [driver.name, round(driver.all_distance), driver.fuel_saved, driver.money_saved, payable, ""]
            table_data.append(driver_params)
        summed = ["Összesen", round(all_distance), round(all_saved_fuel, 2), possible_money_saved, all_money, ""]
        table_data.append(summed)
        return table_data





