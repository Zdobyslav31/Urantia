import pygame

ASSET_PATH = 'images/'


class AssetLibrary:
    def __init__(self):
        self.asset_dict = {
            'background': 'background_bronze.jpg',
            'speedometer': 'speedometer.png',
            'clock_hand': 'clock_hand.png',
            'indicator_background': 'indicator_panel.png',
            'indicator_hand': 'indicator_hand.png',
            'gauge_background': 'gauge_bg.png',
            'gauge_hand': 'clock_hand.png',
        }

    def path(self, asset_name):
        return ASSET_PATH + self.asset_dict[asset_name]

    def load(self, asset_name):
        return pygame.image.load(self.path(asset_name))


assets = AssetLibrary()
