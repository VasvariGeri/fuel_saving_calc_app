
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

    def calc_norma(self):
        if self.formula is not None:
            formatted_formula = self.formula
            formatted_formula = formatted_formula.replace("Gm", str(self.total_weight))
            formatted_formula = formatted_formula.replace("Gs", str(self.self_weight))
            formatted_formula = formatted_formula.replace("N", str(self.performance))
            formatted_formula = formatted_formula.replace("0,", ".")
            formatted_formula = formatted_formula.replace(",", ".")
            return round(eval(formatted_formula), 2)
        else:
            return None

    def calc_all_consumption_by_norma(self, norma):
        if norma is not None:
            return (self.distance_covered * norma) / 100 + self.cooling_time * 3
        else:
            return 0

