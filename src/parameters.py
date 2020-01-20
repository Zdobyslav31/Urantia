import pygame

from src.devices import LevelIndicator, Gauge, Compass, HorizontalSnapIndicator, TurnIndicator


PARAMETERS = {
    # Parameters connected with changing height
    'height': {
        'initial_value': 0,
        'min_value': 0,
        'max_value': 3000,
        'max_step': 7,
        'device': {
            'class': LevelIndicator,
            'coordinates': (100, 50),
        }
    },
    'destined_height': {
        'initial_value': 0,
        'min_value': -200,
        'max_value': 3000,
    },
    'pressure': {
        'initial_value': 3800,
        'min_value': 800,
        'max_value': 4000,
        'controller': {
            'step': 10,
            'increase': pygame.K_p,
            'decrease': pygame.K_l
        },
        'device': {
            'class': Gauge,
            'coordinates': (50, 900),
        }

    },
    'pressure_change': {
        'initial_value': 0,
        'min_value': -10,
        'max_value': 10,
    },

    # Parameters connected with moving forward
    'engine_power': {
        'initial_value': 0,
        'min_value': -80,
        'max_value': 80,
        'controller': {
            'step': 1,
            'increase': pygame.K_w,
            'decrease': pygame.K_s
        },
        'device': {
            'class': HorizontalSnapIndicator,
            'coordinates': (700, 1100),
        }
    },
    'velocity': {
        'initial_value': 0,
        'min_value': 0,
        'max_value': 80,
        'device': {
            'class': Gauge,
            'coordinates': (400, 250),
        }
    },
    'acceleration': {
        'initial_value': 0,
        'min_value': -80,
        'max_value': 80,
    },
    'destined_velocity': {
        'initial_value': 0,
        'min_value': -80,
        'max_value': 80,
    },
    'fuel_consumption': {
        'initial_value': 0,
        'min_value': 0,
        'max_value': 80,
        'step': 5,
        'device': {
            'class': Gauge,
            'coordinates': (850, 500),
        }

    },
    'fuel': {
        'initial_value':  500,
        'min_value': 0,
        'max_value': 500,
        'device': {
            'class': LevelIndicator,
            'coordinates': (1300, 50),
        }
    },
    'turn': {
        'initial_value': 0,
        'min_value': -1,
        'max_value': 1,
        'device': {
            'class': TurnIndicator,
            'coordinates': (1900, 900),
        }

    },

    # Parameters connected with turning
    'angular_velocity': {
        'initial_value': 0,
        'min_value': -30,
        'max_value': 30,
        'controller': {
            'step': 1,
            'increase': pygame.K_d,
            'decrease': pygame.K_a
        },
        'device': {
            'class': HorizontalSnapIndicator,
            'coordinates': (1600, 700),
        }
    },
    'direction': {
        'initial_value': 0,
        'min_value': 0,
        'max_value': 360,
        'device': {
            'class': Compass,
            'coordinates': (1820, 200),
        }
    },
    'coordinates': {
        'initial_value': (0, 0)
    }
}


class Parameter:
    """Basic parameter of a zeppelin"""
    def __init__(self, snap=None):
        self.value = None
        self.min_value = None
        self.max_value  =None
        if snap is not None:
            self.snapping_enabled = True
            self.snap_to = snap
        else:
            self.snapping_enabled = False

    def set_range(self, min_value, max_value):
        """Function called once  in the beginning, to set the max range"""
        self.min_value = min_value
        self.max_value = max_value

    def get_range(self):
        return self.min_value, self.max_value

    def set_value(self, value):
        """Set value so that it fits in parameter's range limits"""
        if value > self.max_value:
            self.value = self.max_value
        elif value < self.min_value:
            self.value = self.min_value
        else:
            self.value = value

    def get_value(self):
        return self.value

    def change(self, number, hard=False):
        """Increase the value by number"""
        if self.snapping_enabled and self.value == self.snap_to and not hard:
            return
        self.set_value(self.value + number)


class DirectionParameter(Parameter):
    """Continuous parameter, used for direction (0-360) implementation"""
    def __init__(self, value=0, min_value=0, max_value=360, snap=None):
        Parameter.__init__(self, snap=snap)

    def set_value(self, value):
        if value >= self.max_value:
            self.set_value(value - self.max_value)
        elif value < self.min_value:
            self.set_value(value + self.max_value)
        else:
            self.value = value


class TurnedParameter(Parameter):
    """Parameter that can have positive or  negative values, but the negative ones are hidden by default"""
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

    def get_range(self):
        return 0, self.max_value


class HeightParameter(Parameter):
    """Parameter with crash control, when 0 level is achieved too fast"""
    def change(self, number, hard=False):
        crash = None
        if self.value != self.min_value and self.value + number <= self.min_value and number <= -5:
            print("Łup!")
            crash = True
        if self.snapping_enabled and self.value == self.snap_to and not hard:
            return
        self.set_value(self.value + number)
        return crash

class TwoDimensionalParameter(Parameter):
    """
    Parameter of two values, used for zeppelin coordinates implementation
    Self.value is a tuple
    This object does not implement min_value and max_value
    """
    def __init__(self, snap=None):
        super().__init__(snap=snap)
        self.value = (None, None)

    def get_range(self):
        return None, None

    def set_value(self, values: tuple):
        """Set value so that it fits in parameter's range limits"""
        self.value = (values[0], values[1])

    def get_value(self):
        return self.value

    def change(self, numbers: tuple, hard=False):
        """Increase the value by numbers"""
        self.set_value((self.value[0] + numbers[0], self.value[1] + numbers[1]))
