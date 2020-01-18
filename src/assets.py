import pygame

IMAGES_PATH = 'assets/images/'
SOUNDS_PATH = 'assets/sounds/'


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
            'compass_background': 'compass_bg.png',
            'compass_hand': 'compass_shield.png',
            'horizontal_background': 'horizontal_indicator_bg.png',
            'horizontal_hand': 'horizontal_indicator_hand.png',
            'turn_background': 'turn_indicator_bg.png',
            'turn_hand': 'turn_indicator_hand.png'
        }

    def load_image(self, asset_name):
        return pygame.image.load(IMAGES_PATH + self.asset_dict[asset_name])


assets = AssetLibrary()


class Sound:
    def __init__(self, filename, values_range):
        self.file = pygame.mixer.Sound(SOUNDS_PATH + filename)
        self.playing = False
        self.min_value = values_range[0]
        self.max_value = values_range[1]

    def start_playing(self):
        self.file.play(loops=-1)
        self.playing = True

    def set_volume_by_value(self, value):
        self.file.set_volume(self.calculate_volume_for_value(value))

    def calculate_volume_for_value(self, value):
        current_range = (value - self.min_value)
        full_range = (self.max_value - self.min_value)
        return current_range / full_range

    def stop_playing(self):
        self.file.fadeout(500)
        self.playing = False


class SoundController:
    def __init__(self, zeppelin):
        self.asset_dict = {
            'pressure_change': 'diffuser.ogg',
            'engine_power': 'engine.wav',
            'velocity': 'cabin.wav',
        }
        self.zeppelin = zeppelin
        self.sounds = {}
        for parameter, filename in self.asset_dict.items():
            self.sounds[parameter] = Sound(filename, zeppelin.get_range(parameter))

    def update_sounds(self):
        for parameter, sound in self.sounds.items():
            value = self.zeppelin.get_parameter(parameter)
            if not value:
                if sound.playing:
                    sound.stop_playing()
            else:
                sound.set_volume_by_value(value)
                if not sound.playing:
                    sound.start_playing()




