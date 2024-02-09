
class Driver:
    def __init__(self, name):
        self.name = name
        self.trucks_driven = {}
        self.fuel_saved = 0


class Truck:
    def __init__(self, plate_nr):
        self.plate_nr = plate_nr
        self.distance_covered = 0
        self.fuel_tanked = 0
        self.cooling_time = 0
        self.year = None
        self.total_weight = None
        self.self_weight = None
        self.formula = None
        self.performance = None
        self.norma = None

    def calc_norma(self):
        if self.formula is not None:
            formatted_formula = self.formula
            formatted_formula = formatted_formula.replace("Gm", str(self.total_weight))
            formatted_formula = formatted_formula.replace("Gs", str(self.self_weight))
            formatted_formula = formatted_formula.replace("N", str(self.performance))
            formatted_formula = formatted_formula.replace("0,", ".")
            formatted_formula = formatted_formula.replace(",", ".")
            self.norma = round(eval(formatted_formula), 2)

