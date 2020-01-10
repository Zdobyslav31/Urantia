import pygame


class EventManager:

    def __init__(self, zeppelin, display):
        self.zeppelin = zeppelin
        self.display = display

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                self.zeppelin.increase_parameter('height')
            if event.key == pygame.K_b:
                self.zeppelin.decrease_parameter('height')


