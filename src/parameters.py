import pygame

from src.devices import LevelIndicator, Gauge, Compass, HorizontalSnapIndicator, TurnIndicator

PRESSURE_PER_1_FUEL_UNIT = 6000
ACCELERATION_DIVIDER = 20
DECELERATION_LIMIT = -0.3
HEIGHT_CHANGE_DIVIDER = 20
MINIMAL_STEP = 0.2

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
    'destined_velocity': {
        'initial_value': 0,
        'min_value': -80,
        'max_value': 80,
    },
    'fuel_consumption': {
        'initial_value': 0,
        'min_value': 0,
        'max_value': 50,
        'device': {
            'class': Gauge,
            'coordinates': (850, 500),
        }

    },
    'fuel': {
        'initial_value': 100,
        'min_value': 0,
        'max_value': 100,
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
}
