import pandas as pd
from models import Truck, Driver
from helpers import FileReaderHelper
from config import ConfigHelper


class FuelSavingManager:
    def __init__(self, year, month):
        self.trucks = {}
        self.drivers = {}
        self.file_reader = FileReaderHelper(year, month)

    def get_trucks(self):
        mol_riport = self.file_reader.read_riport_file()
        for index, row in mol_riport.iterrows():
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

    def _get_truck_by_plate_nr(self, plate_nr):
        return self.trucks.get(plate_nr)

    def _get_truck_by_driver(self, driver_name, plate_nr):
        return self.drivers[driver_name].trucks_driven.get(plate_nr)

    def process_waybills(self, year, month):
        waybills = self.file_reader.read_waybill_file(self.trucks.keys())
        for plate_nr, waybill in waybills.items():
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


def main():
    config = ConfigHelper()
    manager = FuelSavingManager(config.YEAR, config.MONTH)
    manager.get_trucks()
    manager.process_waybills(config.YEAR, config.MONTH)


if __name__ == "__main__":
    main()
