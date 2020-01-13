from src.parameters import PARAMETERS


class Parameter:
    def __init__(self, value=0, min_value=0, max_value=0, snap=None):
        self.value = None
        self.min_value = min_value
        self.max_value = max_value
        self.set_value(value)
        if snap is not None:
            self.snapping_enabled = True
            self.snap_to = snap
        else:
            self.snapping_enabled = False

    def set_range(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def set_value(self, value):
        if value > self.max_value:
            self.value = self.max_value
        elif value < self.min_value:
            self.value = self.min_value
        else:
            self.value = value

    def change(self, number, hard=False):
        if self.snapping_enabled and self.value == self.snap_to and not hard:
            return
        self.set_value(self.value + number)


class DirectionParameter(Parameter):
    def __init__(self, value=0, min_value=0, max_value=360, snap=None):
        Parameter.__init__(self, value, min_value, max_value, snap=snap)

    def set_value(self, value):
        if value >= self.max_value:
            self.set_value(value - self.max_value)
        elif value < self.min_value:
            self.set_value(value + self.max_value)
        else:
            self.value = value


class Zeppelin:
    def __init__(self):
        self.parameters = {
            'pressure': Parameter(),
            'height': Parameter(),
            'destined_height': Parameter(),
            'engine_power': Parameter(snap=0),
            'acceleration': Parameter(),
            'destined_velocity': Parameter(),
            'velocity': Parameter(),
            'fuel_consumption': Parameter(),
            'fuel': Parameter(),
            'angular_velocity': Parameter(snap=0),
            'direction': DirectionParameter(),
        }
        for parameter, data in PARAMETERS.items():
            self.parameters[parameter].set_range(data['min_value'], data['max_value'])
            self.parameters[parameter].set_value(data['initial_value'])

    def get_parameter(self, parameter):
        return self.parameters[parameter].value

    def change_parameter(self, parameter, value, hard=False):
        self.parameters[parameter].change(value, hard=hard)

