import pygame

from display_manager import DisplayManager
from event_manager import EventManager
from zeppelin import Zeppelin

FPS = 30

class Game:
    def __init__(self):
        self.running = True
        self.zeppelin = Zeppelin()
        self.display_manager = DisplayManager(self.zeppelin)
        self.event_manager = EventManager(self.zeppelin, self.display_manager)

    def run(self):
        while self.running:
            self.controller_tick()
            self.view_tick()

    def controller_tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.running = False
            else:
                self.event_manager.process_event(event)
        return

    def view_tick(self):
        pass
