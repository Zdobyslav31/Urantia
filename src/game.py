import pygame

from src.display_manager import DisplayManager
from src.event_manager import EventManager
from src.zeppelin import Zeppelin


class Game:
    def __init__(self):
        self.running = True
        self.zeppelin = Zeppelin()
        self.display_manager = DisplayManager(self.zeppelin)
        self.event_manager = EventManager(self.zeppelin)

    def run(self):
        while self.running:
            self.controller_tick()
            self.view_tick()

    def controller_tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.event_manager.process_event(event.key)
        keys = pygame.key.get_pressed()
        if sum(keys):
            for index in range(len(keys)):
                if keys[index]:
                    self.event_manager.process_event(index)

    def view_tick(self):
        self.display_manager.update_display()
