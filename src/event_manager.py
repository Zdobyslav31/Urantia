import pygame


class EventManager:

    def __init__(self, zeppelin, display):
        self.zeppelin = zeppelin
        self.display = display

    def process_event(self, key):
        if key == pygame.K_h:
            self.zeppelin.increase_parameter('height')
        if key == pygame.K_b:
            self.zeppelin.decrease_parameter('height')


