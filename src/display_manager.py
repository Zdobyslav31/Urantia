import pygame

from src.assets import assets
from src.parameters import PARAMETERS

FULLSCREEN = False
SCREEN_SIZE = (2560, 1440)


class DisplayManager:
    def __init__(self, zeppelin):
        self.zeppelin = zeppelin
        pygame.display.set_mode(SCREEN_SIZE if SCREEN_SIZE else (0, 0), pygame.FULLSCREEN if FULLSCREEN else 0)
        self.screen = pygame.display.get_surface()
        self.initialize_background()
        self.devices = {}
        self.initialize_devices()
        pygame.display.flip()

    def update_display(self):
        for parameter, device in self.devices.items():
            device.update(self.zeppelin.get_parameter(parameter))
            self.screen.blit(device.image, device.position)
        pygame.display.flip()

    def initialize_background(self):
        background = assets.load('background')
        self.screen.blit(background, (0, 0))

    def initialize_devices(self):
        for parameter, data in PARAMETERS.items():
            self.devices[parameter] = data['device']['class'](
                values_range=(data['min_value'], data['max_value']),
                coordinates=data['device']['coordinates'],
                initial_value=data['initial_value'],
            )




