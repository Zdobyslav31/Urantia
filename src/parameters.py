from src.devices import LevelIndicator

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
        'step': 10,
        'device': {
            'class': LevelIndicator,
            'coordinates': (30, 30),
        }

    }
}