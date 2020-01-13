import pygame

from src.devices import LevelIndicator, Gauge, Compass, HorizontalSnapIndicator


PARAMETERS = {
    'height': {
        'initial_value': 0,
        'min_value': 0,
        'max_value': 3000,
        'device': {
            'class': LevelIndicator,
            'coordinates': (100, 50),
        }
    },
    'pressure': {
        'initial_value': 1500,
        'min_value': 700,
        'max_value': 2000,
        'controller': {
            'step': 2,
            'increase': pygame.K_p,
            'decrease': pygame.K_l
        },
        'device': {
            'class': Gauge,
            'coordinates': (50, 900),
        }

    },
    'engine_power': {
        'initial_value': 0,
        'min_value': -100,
        'max_value': 100,
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
    'angular_velocity': {
        'initial_value': 0,
        'min_value': -30,
        'max_value': 30,
        'controller': {
            'step': 1,
            'increase': pygame.K_a,
            'decrease': pygame.K_d
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
