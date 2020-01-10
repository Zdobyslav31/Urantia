from src.parameters import PARAMETERS


class Parameter:
    def __init__(self, value, min_value, max_value, step):
        self.value = None
        self.min_value = min_value
        self.max_value = max_value
        self.set_value(value)
        self.step = step

    def set_value(self, value):
        if value > self.max_value:
            self.value = self.max_value
        elif value < self.min_value:
            self.value = self.min_value
        else:
            self.value = value

    def increase(self):
        self.set_value(self.value + self.step)

    def decrease(self):
        self.set_value(self.value - self.step)


class Zeppelin:
    def __init__(self):
        self.parameters = {}
        for parameter, data in PARAMETERS.items():
            self.parameters[parameter] = Parameter(
                data['initial_value'],
                data['min_value'],
                data['max_value'],
                data['step']
            )

    def get_parameter(self, parameter):
        return self.parameters[parameter].value

    def increase_parameter(self, parameter):
        self.parameters[parameter].increase()

    def decrease_parameter(self, parameter):
        self.parameters[parameter].decrease()

