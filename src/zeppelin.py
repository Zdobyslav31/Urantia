from src.parameters import *
from src.const import *


class Zeppelin:
    """Object representing the zeppelin with all its parameters"""
    def __init__(self):
        self.parameters = {
            'pressure': Parameter(),
            'height': HeightParameter(),
            'destined_height': Parameter(),
            'engine_power': Parameter(snap=0),
            'acceleration': Parameter(),
            'destined_velocity': Parameter(),
            'velocity': TurnedParameter(),
            'fuel_consumption': Parameter(),
            'fuel': Parameter(),
            'turn': Parameter(),
            'angular_velocity': Parameter(snap=0),
            'direction': DirectionParameter(),
            'pressure_change': TurnedParameter(),
        }

        for parameter, data in PARAMETERS.items():
            self.parameters[parameter].set_range(data['min_value'], data['max_value'])
            self.parameters[parameter].set_value(data['initial_value'])

        self.pressure_cache = self.get_parameter('pressure')
        self.engine_cache = self.get_parameter('engine_power')
        self.fuel_consumption_cache = 0
        self.distance_travelled = 0
        self.pressure_change = 0
        self.velocity_difference = 0

        self.crashed = None

    def get_parameter(self, parameter):
        return self.parameters[parameter].get_value()

    def get_range(self, parameter):
        return self.parameters[parameter].get_range()

    def get_turned_velocity(self):
        return self.parameters['velocity'].get_turned_value()

    def change_parameter(self, parameter, value, hard=False):
        crash = self.parameters[parameter].change(value, hard=hard)
        if crash:
            self.crashed = True

    def set_parameter(self, parameter, value):
        self.parameters[parameter].set_value(value)

    def update_values(self, milliseconds):
        """Function updates all the values, that are calculated on the basis of other parameters"""

        # If pressure has changed, update destined_height
        self.set_parameter('pressure_change', abs(self.pressure_cache - self.get_parameter('pressure')))
        if self.get_parameter('pressure_change'):
            self.pressure_cache = self.get_parameter('pressure')
            self.set_parameter('destined_height', self.get_height_from_pressure())

        # If height != destined_height, update height
        height_difference = self.get_parameter('destined_height') - self.get_parameter('height')
        if abs(height_difference) > 0:
            # If difference is minimal, just set the destined value to prevent infinite loop
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
            # when the zeppelin touches the ground, set destined_parameter to zero
            # so that it doesn't force to calculate height_change every time
            if self.get_parameter('height') == self.parameters['height'].min_value:
                self.set_parameter('destined_height', self.get_parameter('height'))

        # If engine_power has changed, update destined_velocity and acceleration
        engine_change = abs(self.engine_cache - self.get_parameter('engine_power'))
        if engine_change:
            self.engine_cache = self.get_parameter('pressure')
            self.set_parameter('destined_velocity', self.get_velocity_from_engine_power())

        # If velocity != destined_velocity, update velocity and turn
        self.velocity_difference = self.get_parameter('destined_velocity') - self.get_turned_velocity()
        if abs(self.velocity_difference) > 0:
            # If difference is minimal, stop the changes to prevent infinite loop
            if abs(self.velocity_difference) < MINIMAL_STEP:
                self.set_parameter('velocity', self.get_parameter('destined_velocity'))
            else:
                self.set_parameter('acceleration', self.get_acceleration())
                self.change_parameter(
                    'velocity',
                    self.get_parameter('acceleration')
                )
            self.set_parameter('turn', self.get_turn())


        # Update direction based on angular_velocity and velocity
        if self.get_parameter('angular_velocity'):
            self.change_parameter(
                'direction',
                self.get_parameter('angular_velocity') * self.get_turned_velocity() / 500
            )

        # Calculate fuel consumption
        self.fuel_consumption_cache = self.calculate_fuel_consumption()
        self.set_parameter('fuel_consumption', self.fuel_consumption_cache)

        # Calculate the distance
        distance = self.get_parameter('velocity') * milliseconds / 1000 / 3600
        self.distance_travelled += distance

        # Calculate how much fuel has been consumed during last frame
        consumed_fuel = distance * self.get_parameter('fuel_consumption') / 10
        self.change_parameter('fuel', -consumed_fuel)

    def get_turn(self):
        return self.parameters['velocity'].get_turn()

    def get_height_from_pressure(self):
        """Return the height value that is destined for the current pressure"""
        pressure = self.get_parameter('pressure')
        return PARAMETERS['pressure']['initial_value'] - pressure

    def get_velocity_from_engine_power(self):
        """Return the velocity value that is destined for the current engine power"""
        return self.get_parameter('engine_power')

    def get_acceleration(self):
        """Return the acceleration value that emerges from the current velocity difference"""
        if not self.is_accelerating():
            return self.get_velocity_lambda_turn() * min(
                abs(self.velocity_difference) / ACCELERATION_DIVIDER / 3,
                DECELERATION_LIMIT
            )
        if self.get_velocity_lambda_turn() > 0:
            return self.velocity_difference / ACCELERATION_DIVIDER
        else:
            return self.velocity_difference / ACCELERATION_DIVIDER / 3

    def is_accelerating(self):
        """Check if the zeppelin is currently actively increasing its velocity"""
        v = self.get_turned_velocity()
        dv = self.get_parameter('destined_velocity')
        if dv == 0:
            return False
        if v * dv < 0:
            return True
        if abs(dv) > abs(v):
            return True
        return False

    def get_velocity_lambda_turn(self):
        """Check the turn of the current velocity_difference"""
        v = self.get_turned_velocity()
        dv = self.get_parameter('destined_velocity')
        if dv > v:
            return 1
        if dv < v:
            return -1
        return 0

    def calculate_fuel_consumption(self):
        """Calculates the current fuel_consumption based on engine power,  acceleration and pressure_change"""

        # Calculate the base consumption that emerges from the engine power
        consumption = self.fuel_consumption_from_engine_power()

        # Include positive modifier for active acceleration
        if self.is_accelerating():
            consumption += abs(self.velocity_difference) / ACCELERATION_MODIFIER_DIVIDER

        # Include negative modifier for passive deceleration
        else:
            consumption -= abs(self.velocity_difference) / DECELERATION_MODIFIER_DIVIDER

        # Include fuel consumed by changing pressure
        if self.get_parameter('pressure_change'):
            consumption += abs(self.get_parameter('pressure_change')) / PRESSURE_DIVIDER_MODIFIER

        # Limit the ultimate value to the max step, so thet the indicator hand goes smoothly
        if consumption - self.fuel_consumption_cache > PARAMETERS['fuel_consumption']['step']:
            consumption = self.fuel_consumption_cache + PARAMETERS['fuel_consumption']['step']
        elif self.fuel_consumption_cache - consumption > PARAMETERS['fuel_consumption']['step']:
            consumption = self.fuel_consumption_cache - PARAMETERS['fuel_consumption']['step']

        return consumption

    def fuel_consumption_from_engine_power(self):
        """Calculates the basic consumption based on engine power"""
        power = abs(self.get_parameter('engine_power'))
        if power == 0:
            return 0
        return (power - 50) ** 2 / 125 + 10

    def print_values(self):
        print("_________\nCurrent values:")
        for parameter, data in self.parameters.items():
            print('{:20}: {}'.format(parameter, data.get_value()))
        print('distance_travelled  : {}'.format(self.distance_travelled))
        print('turned_velocity     : {}'.format(self.get_turned_velocity()))
        print('is_accelerating     : {}'.format(self.is_accelerating()))
        print('v_lambda_turn       : {}'.format(self.get_velocity_lambda_turn()))
        print('CRASHED             : {}'.format(self.crashed))
