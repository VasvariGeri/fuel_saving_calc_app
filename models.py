
class Driver:
    def __init__(self, name):
        self.name = name
        self.trucks_driven = {}
        self.distance_driven = 0
        self.fuel_saved = 0


class Truck:
    def __init__(self, plate_nr):
        self.plate_nr = plate_nr
        self.distance_covered = 0
        self.fuel_tanked = 0
