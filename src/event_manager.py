import pygame

from src.parameters import PARAMETERS


class EventManager:

    def __init__(self, zeppelin):
        self.zeppelin = zeppelin
        self.key_dict = {}
        self.initialize_keys()

    def initialize_keys(self):
        for parameter, data in PARAMETERS.items():
            if 'controller' in data:
                controller = data['controller']
                step = controller['step']
                if 'increase' in controller:
                    self.key_dict[controller['increase']] = self.zeppelin_parameter_changers_generator(parameter, step)
                if 'decrease' in controller:
                    self.key_dict[controller['decrease']] = self.zeppelin_parameter_changers_generator(parameter, -step)

    @staticmethod
    def zeppelin_parameter_changers_generator(parameter, value):
        """Return an anonymous function that will call change_parameter on a given zeppelin object"""
        def changer(zeppelin, hard=False):
            zeppelin.change_parameter(parameter, value, hard=hard)
        return changer

    def process_event(self, key, hard=False):
        if key in self.key_dict:
            self.key_dict[key](self.zeppelin, hard=hard)


