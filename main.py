import pandas as pd
import datetime
from tkinter import messagebox
from models import Truck, Driver
from helpers import FileReaderHelper
from config import ConfigHelper


class FuelSavingManager:
    def __init__(self, year, month):
        self.trucks = {}
        self.drivers = {}
        self.file_reader = FileReaderHelper(year, month)
        self.mol_riport = self.file_reader.read_riport_file()
        self._get_trucks()
        self.waybills = self.file_reader.read_waybill_file(self.trucks.keys())
        self.norma = self.file_reader.read_norma_file()
        self.all_distance = 0

    def _get_trucks(self):
        for index, row in self.mol_riport.iterrows():
            plate_nr = row["Rendszám"]
            if pd.notna(plate_nr):
                if plate_nr not in self.trucks.keys():
                    truck = Truck(plate_nr)
                    truck.fuel_tanked = row["Mennyiség"]
                    self.trucks[plate_nr] = truck
                elif self.trucks[plate_nr]:
                    self.trucks[plate_nr].fuel_tanked += row["Mennyiség"]

    def _get_truck_by_plate_nr(self, plate_nr):
        return self.trucks.get(plate_nr)

    def _get_truck_by_driver(self, driver_name, plate_nr):
        return self.drivers[driver_name].trucks_driven.get(plate_nr)

    def process_waybills(self, year, month):
        for plate_nr, waybill in self.waybills.items():
            for index, row in waybill.iterrows():
                driver_name = row["Név"]
                if row["Év"] == year and row["Hónap"] == month and pd.notna(driver_name):
                    distance = row["Tényleges km"]
                    if self.drivers.get(driver_name) is None:
                        driver = Driver(driver_name)
                        driver.trucks_driven[plate_nr] = distance
                        self.drivers[driver_name] = driver
                    elif self._get_truck_by_driver(driver_name, plate_nr) is None:
                        self.drivers[driver_name].trucks_driven[plate_nr] = distance
                    else:
                        self.drivers[driver_name].trucks_driven[plate_nr] += distance
                    truck = self._get_truck_by_plate_nr(plate_nr)
                    truck.distance_covered += distance
                    truck.cooling_time += row["Hűtés"]

    def process_norma_file(self):
        errors = []
        for plate_nr in self.trucks:
            truck_details = self.norma.get(plate_nr)
            if truck_details is not None:
                truck = self.trucks[plate_nr]
                truck.year = truck_details["gyártás éve"]
                truck.total_weight = truck_details["megengedett legnagyobb össztömeg"]
                truck.self_weight = truck_details["saját tömeg"]
                truck.formula = truck_details["számítás"]
                truck.performance = truck_details["motorteljesítmény"]
            else:
                errors.append(plate_nr)
        if errors:
            errors_message = "\n".join(errors)
            messagebox.showerror("Error", f"Missing norma info:\n{errors_message}")

    def _calc_consumption_diff(self):
        all_consumption_by_norma = 0
        all_consumption_real = 0
        for plate_nr in self.trucks:
            truck = self.trucks[plate_nr]
            self.all_distance += truck.distance_covered
            norma = truck.calc_norma()
            all_consumption_by_norma += truck.calc_all_consumption_by_norma(norma)
            all_consumption_real += truck.fuel_tanked
        return round(all_consumption_by_norma - all_consumption_real)

    def main_calculation(self):
        consumption_diff = self._calc_consumption_diff()
        print(consumption_diff)


def main():
    start = datetime.datetime.now()
    config = ConfigHelper()
    config.display_gui()
    manager = FuelSavingManager(config.YEAR, config.MONTH)
    manager.process_waybills(config.YEAR, config.MONTH)
    manager.process_norma_file()
    manager.main_calculation()
    config.root.destroy()
    end = datetime.datetime.now()
    print(end - start)


if __name__ == "__main__":
    main()
