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
        dirty_rects = []
        for parameter, device in self.devices.items():
            device.update(self.zeppelin.get_parameter(parameter))
            rect = self.screen.blit(device.image, device.position)
            dirty_rects.append(rect)
        pygame.display.update(dirty_rects)

    def initialize_background(self):
        background = assets.load_image('background')
        self.screen.blit(background, (0, 0))

    def initialize_devices(self):
        for parameter, data in PARAMETERS.items():
            if 'device' in data:
                self.devices[parameter] = data['device']['class'](
                    values_range=(data['min_value'], data['max_value']),
                    coordinates=data['device']['coordinates'],
                    initial_value=data['initial_value'],
                )

    def black_screen(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()



