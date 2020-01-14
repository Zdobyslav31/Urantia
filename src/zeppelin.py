from src.parameters import *


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

    def get_value(self):
        return self.value

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


class VelocityParameter(Parameter):
    def set_range(self, min_value, max_value):
        self.min_value = -max_value
        self.max_value = max_value

    def get_value(self):
        return abs(self.value)

    def get_turned_value(self):
        return self.value

    def get_turn(self):
        if self.value > 0:
            return 1
        elif self.value < 0:
            return -1
        return 0


class HeightParameter(Parameter):
    def change(self, number, hard=False):
        if self.value != self.min_value and self.value + number <= self.min_value and number <= -5:
            print("Łup!")
        if self.snapping_enabled and self.value == self.snap_to and not hard:
            return
        self.set_value(self.value + number)


class Zeppelin:
    def __init__(self):
        self.parameters = {
            'pressure': Parameter(),
            'height': HeightParameter(),
            'destined_height': Parameter(),
            'engine_power': Parameter(snap=0),
            'acceleration': Parameter(),
            'destined_velocity': Parameter(),
            'velocity': VelocityParameter(),
            'fuel_consumption': Parameter(),
            'fuel': Parameter(),
            'turn': Parameter(),
            'angular_velocity': Parameter(snap=0),
            'direction': DirectionParameter(),
        }

        for parameter, data in PARAMETERS.items():
            self.parameters[parameter].set_range(data['min_value'], data['max_value'])
            self.parameters[parameter].set_value(data['initial_value'])

        self.pressure_cache = self.get_parameter('pressure')
        self.engine_cache = self.get_parameter('engine_power')

    def get_parameter(self, parameter):
        return self.parameters[parameter].get_value()

    def change_parameter(self, parameter, value, hard=False):
        self.parameters[parameter].change(value, hard=hard)

    def set_parameter(self, parameter, value):
        self.parameters[parameter].set_value(value)

    def update_values(self):
        # Update direction based on angular_velocity
        if self.get_parameter('angular_velocity'):
            self.change_parameter('direction', self.get_parameter('angular_velocity')/10)

        # If pressure has changed, update destined_height
        pressure_change = abs(self.pressure_cache - self.get_parameter('pressure'))
        if pressure_change:
            self.change_parameter(  # TODO: temporary add this value to fuel consumption
                'fuel',
                -pressure_change/PRESSURE_PER_1_FUEL_UNIT
            )
            self.pressure_cache = self.get_parameter('pressure')
            self.set_parameter('destined_height', self.get_height_from_pressure())

        # If height != destined_height, update height
        height_difference = self.get_parameter('destined_height') - self.get_parameter('height')
        if abs(height_difference) > 0:
            # If difference is minimal, stop the changes to prevent infinite loop
            if abs(height_difference) < MINIMAL_STEP:
                self.set_parameter('height', self.get_parameter('destined_height'))
            else:
                self.change_parameter(
                    'height',
                    min(
                        height_difference / HEIGHT_CHANGE_DIVIDER,
                        PARAMETERS['height']['max_step']
                    )
                )
            if self.get_parameter('height') == self.parameters['height'].min_value:
                self.set_parameter('destined_height', self.get_parameter('height'))

        # If engine_power has changed, update destined_velocity and acceleration
        engine_change = abs(self.engine_cache - self.get_parameter('engine_power'))
        if engine_change:
            self.engine_cache = self.get_parameter('pressure')
            self.set_parameter('destined_velocity', self.get_velocity_from_engine_power())

        # If velocity (turned) != destined_velocity, update velocity
        velocity_difference = self.get_parameter('destined_velocity') - self.parameters['velocity'].get_turned_value()
        if abs(velocity_difference) > 0:
            # If difference is minimal, stop the changes to prevent infinite loop
            if abs(velocity_difference) < MINIMAL_STEP:
                self.set_parameter('velocity', self.get_parameter('destined_velocity'))
            else:
                self.change_parameter(
                    'velocity',
                    self.get_acceleration(velocity_difference)
                )
            self.set_parameter('turn', self.get_turn())

    def get_turn(self):
        return self.parameters['velocity'].get_turn()

    def get_height_from_pressure(self):
        pressure = self.get_parameter('pressure')
        return PARAMETERS['pressure']['initial_value'] - pressure

    def get_velocity_from_engine_power(self):
        return self.get_parameter('engine_power')

    def get_acceleration(self, velocity_difference):
        if velocity_difference > 0:
            return velocity_difference / ACCELERATION_DIVIDER
        else:
            if self.get_parameter('destined_velocity') > 0:
                return max(velocity_difference / ACCELERATION_DIVIDER / 3, DECELERATION_LIMIT)
            else:
                return velocity_difference / ACCELERATION_DIVIDER / 3


