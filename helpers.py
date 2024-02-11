import os
from pandas import ExcelFile, read_excel
from yaml import safe_load
from tkinter import messagebox
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.tables import TableStyle
from reportlab.lib import colors


class FileIOHelper:

    def read_riport_file(self, year, month):
        riport_filepath = f"./input/Ellenörző riport {year} {month}.xlsx"
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

    def write_payroll_file(self, drivers, all_money, all_distance, year, month, fuel_price, limit):
        output_dir = "./output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filepath = f"./output/Bérfizetési jegyzék {year} {month}.pdf"
        doc = SimpleDocTemplate(filepath)
        elements = self._create_file_elements(drivers, all_money, all_distance, year, month, fuel_price, limit)
        doc.build(elements)

    def _create_file_elements(self, drivers, all_money, all_distance, year, month, fuel_price, limit):
        elements = []
        header = [Paragraph("CUSTODE TRANS KFT"), Paragraph("6100 Kiskunfélegyháza"), Paragraph("Bajcsi-Zsilinszky u. 24")]
        elements.extend(header)
        title_space = Spacer(1, 48)
        space = Spacer(1, 24)
        elements.append(title_space)
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=getSampleStyleSheet()['Title'],
            alignment=1,
        )
        title_text = f"Üzemanyag megtakarítás {year}.{month}"
        title = Paragraph(title_text, style=title_style, encoding="utf-8")
        elements.append(title)
        elements.append(title_space)
        table_data = self._generate_table_data(drivers, all_money, all_distance, limit)
        table_style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add borders to all cells
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Add background color to the header row
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Set text color for the header row
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),  # Make the first line bold
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black)  # Make the last line bold
        ])
        table = Table(table_data, style=table_style)
        elements.append(table)
        elements.append(space)
        elements.append(Paragraph(f"Gázolaj egységár: {fuel_price}"))
        return elements

    def _change_character(self, driver):
        if "ő" in driver.name or "ű" in driver.name:
            driver.name = driver.name.replace("ő", "ö")
            driver.name = driver.name.replace("ű", "ü")

    def _generate_table_data(self, drivers, all_money, all_distance, limit):
        table_data = [["Név", "Teljesített km", "Megtak liter", "Megtak Ft", "Kifizethetö", "Átvételi elismerés"]]
        all_saved_fuel = 0
        possible_money_saved = 0
        for driver in drivers.values():
            all_saved_fuel += driver.fuel_saved
            possible_money_saved += driver.money_saved
            payable = limit if limit < driver.money_saved else driver.money_saved
            self._change_character(driver)
            driver_params = [driver.name, round(driver.all_distance), driver.fuel_saved, driver.money_saved, payable, ""]
            table_data.append(driver_params)
        summed = ["Összesen", round(all_distance), round(all_saved_fuel, 2), possible_money_saved, all_money, ""]
        table_data.append(summed)
        return table_data
