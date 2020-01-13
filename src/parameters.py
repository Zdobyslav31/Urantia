import pygame

from src.devices import LevelIndicator, GaugeIndicator

INITIAL_VALUES = {
    'height': 0,
    'position': (0, 0),
    'velocity': 0,
    'direction': 0,
    'fuel': 100,
}

PARAMETERS = {
    'height': {
        'initial_value': 0,
        'min_value': 0,
        'max_value': 3000,
        'controller': {
            'step': 1,
            'increase': pygame.K_h,
            'decrease': pygame.K_b
        },
        'device': {
            'class': LevelIndicator,
            'coordinates': (30, 30),
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
            'class': GaugeIndicator,
            'coordinates': (250, 30),
        }

    },
    'velocity': {
        'initial_value': 0,
        'min_value': 0,
        'max_value': 80,
        'controller': {
            'step': 0.2,
            'increase': pygame.K_g,
            'decrease': pygame.K_v
        },
        'device': {
            'class': GaugeIndicator,
            'coordinates': (1000, 30),
        }

    }
}
