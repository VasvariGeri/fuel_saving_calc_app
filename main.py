import pandas as pd
from models import Truck, Driver

class FuelSavingManager():
    def __init__(self):
        self.mol_riport = self.read_riport_file()
        self.trucks = {}
        self.drivers = []

    def read_riport_file(self):
        mol_excel_file = pd.ExcelFile("./input/Ellenörző riport 2023 12.xlsx")
        mol_riport_sheets = mol_excel_file.sheet_names
        return pd.read_excel("./input/Ellenörző riport 2023 12.xlsx", sheet_name=mol_riport_sheets[0], parse_dates=True)

    def get_trucks(self):
        for index, row in self.mol_riport.iterrows():
            plate_nr = row["Rendszám"]
            if pd.notna(plate_nr):
                if plate_nr not in self.trucks.keys():
                    truck = Truck(plate_nr)
                    truck.fuel_tanked = row["Mennyiség"]
                    self.trucks[plate_nr] = truck
                elif self.trucks[plate_nr]:
                    self.trucks[plate_nr].fuel_tanked += row["Mennyiség"]
        for truck in self.trucks.values():
            print(truck.plate_nr + ": " + str(truck.fuel_tanked))


if __name__ == "__main__":
    manager = FuelSavingManager()
    manager.get_trucks()
