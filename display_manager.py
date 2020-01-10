import pygame

from assets import AssetLibrary

FULLSCREEN = False
SCREEN_SIZE = (1280, 720)


class DisplayManager:
    def __init__(self, zeppelin):
        self.zeppelin = zeppelin
        pygame.display.set_mode(SCREEN_SIZE if SCREEN_SIZE else (0, 0), pygame.FULLSCREEN if FULLSCREEN else 0)
        self.screen = pygame.display.get_surface()
        self.assets = AssetLibrary()
        self.initialize_background()
        self.initialize_devices()

    def initialize_background(self):
        background = self.assets.load('background')
        self.screen.blit(background, (0, 0))
        pygame.display.flip()

    def initialize_devices(self):
        speedometer = Speedometer(self.assets)
        speedometer.draw_device(self.zeppelin.velocity)
        pygame.display.flip()


class Speedometer:
    def __init__(self, assets):
        self.coordinates = (30, 30)
        self.panel_image = assets.load('speedometer')
        self.indicator_image = assets.load('clock_hand')

    def draw_device(self, value):
        screen = pygame.display.get_surface()
        screen.blit(self.panel_image, self.coordinates)

