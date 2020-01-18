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
    def __init__(self, filename):
        self.file = pygame.mixer.Sound(SOUNDS_PATH + filename)
        self.playing = False

    def start_playing(self):
        self.file.play()
        self.playing = True

    def stop_playing(self):
        self.file.stop()
        self.playing = False


class ParameterSound(Sound):
    def __init__(self, filename, values_range):
        super().__init__(filename)
        self.min_value = values_range[0]
        self.max_value = values_range[1]

    def start_playing(self):
        self.file.play(loops=-1)
        self.playing = True

    def set_volume_by_value(self, value):
        self.file.set_volume(self.calculate_volume_for_value(value))

    def calculate_volume_for_value(self, value):
        return value / self.max_value

    def stop_playing(self):
        self.file.fadeout(100)
        self.playing = False


class SoundController:
    def __init__(self, zeppelin):
        self.parameter_sound_files = {
            'pressure_change': 'diffuser.ogg',
            'engine_power': 'engine.ogg',
            'velocity': 'cabin.ogg',
        }
        self.other_sounds = {
            'crash': 'crash.wav'
        }
        self.zeppelin = zeppelin
        self.parameter_sounds = {}
        self.sounds = {}
        for parameter, filename in self.parameter_sound_files.items():
            self.parameter_sounds[parameter] = ParameterSound(filename, zeppelin.get_range(parameter))
        for name, filename in self.other_sounds.items():
            self.sounds[name] = Sound(filename)

    def update_sounds(self):
        for parameter, sound in self.parameter_sounds.items():
            value = abs(self.zeppelin.get_parameter(parameter))
            if not value:
                if sound.playing:
                    sound.stop_playing()
            else:
                sound.set_volume_by_value(value)
                if not sound.playing:
                    sound.start_playing()

    def crash_sound(self):
        for parameter, sound in self.parameter_sounds.items():
            if sound.playing:
                sound.stop_playing()
        if not self.sounds['crash'].playing:
            self.sounds['crash'].start_playing()



