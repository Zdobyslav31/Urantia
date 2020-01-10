import pygame


class EventManager:

    def __init__(self, zeppelin):
        self.zeppelin = zeppelin

    def process_event(self, key):
        if key == pygame.K_h:
            self.zeppelin.increase_parameter('height')
        if key == pygame.K_b:
            self.zeppelin.decrease_parameter('height')


