from pandas import notna
from tkinter import messagebox
from models import Truck, Driver
from helpers import FileIOHelper
from config import ConfigHelper


class FuelSavingManager:
    def __init__(self, year, month, fuel_price, limit):
        self.trucks = {}
        self.drivers = {}
        self.file_reader = FileIOHelper(year, month, fuel_price, limit)
        self.all_distance = 0
        self.all_money_saved = 0

    def _process_mol_riport(self):
        mol_riport = self.file_reader.read_riport_file()
        for index, row in mol_riport.iterrows():
            plate_nr = row["Rendszám"]
            if notna(plate_nr):
                if self.trucks.get(plate_nr) is None:
                    truck = Truck(plate_nr)
                    truck.fuel_tanked = row["Mennyiség"]
                    self.trucks[plate_nr] = truck
                else:
                    self.trucks[plate_nr].fuel_tanked += row["Mennyiség"]

    def _get_truck_by_plate_nr(self, plate_nr):
        return self.trucks.get(plate_nr)

    def _get_truck_by_driver(self, driver_name, plate_nr):
        return self.drivers[driver_name].trucks_driven.get(plate_nr)

    def _process_waybills(self, year, month):
        waybills = self.file_reader.read_waybill_file()
        for plate_nr, waybill in waybills.items():
            if self.trucks.get(plate_nr) is None:
                self.trucks[plate_nr] = Truck(plate_nr)
            for index, row in waybill.iterrows():
                driver_name = row["Név"]
                if row["Év"] == year and row["Hónap"] == month and notna(driver_name):
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

    def _process_norma_file(self):
        norma = self.file_reader.read_norma_file()
        errors = []
        for plate_nr in self.trucks:
            truck_details = norma.get(plate_nr)
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

    def process_files(self, year, month):
        self._process_mol_riport()
        self._process_waybills(year, month)
        self._process_norma_file()

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

    def _calc_average_saving_per_km(self, consumption_diff):
        return consumption_diff / self.all_distance

    def _calc_savings(self, average_saving, fuel_price, limit):
        for driver_name in self.drivers:
            driver = self.drivers[driver_name]
            driver.fuel_saved = round(average_saving * driver.calc_distance_covered(), 2)
            driver.money_saved = round(driver.fuel_saved * fuel_price)
            if driver.money_saved < limit:
                self.all_money_saved += driver.money_saved
            else:
                self.all_money_saved += limit

    def main_calculation(self, fuel_price, limit):
        consumption_diff = self._calc_consumption_diff()
        average_saving_per_km = self._calc_average_saving_per_km(consumption_diff)
        self._calc_savings(average_saving_per_km, fuel_price, limit)

    def file_writing(self):
        self.file_reader.write_payroll_file(self.drivers, self.all_money_saved, self.all_distance)


def main():
    config = ConfigHelper()
    config.display_gui()
    manager = FuelSavingManager(config.YEAR, config.MONTH, config.FUEL_PRICE, config.LIMIT)
    manager.process_files(config.YEAR, config.MONTH)
    manager.main_calculation(config.FUEL_PRICE, config.LIMIT)
    manager.file_writing()
    config.root.destroy()


if __name__ == "__main__":
    main()
