import pygame

from src.display_manager import DisplayManager
from src.event_manager import EventManager
from src.zeppelin import Zeppelin
from src.assets import SoundController


class Game:
    def __init__(self):
        self.running = True
        self.zeppelin = Zeppelin()
        self.display_manager = DisplayManager(self.zeppelin)
        self.event_manager = EventManager(self.zeppelin)
        self.sound_controller = SoundController(self.zeppelin)
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            milliseconds_passed = self.clock.tick()
            self.controller_tick()
            self.zeppelin.update_values(milliseconds_passed)
            if self.zeppelin.crashed:
                self.game_over()
            self.view_tick()
            self.sound_tick()

    def game_over(self):
        while self.running:
            milliseconds_passed = self.clock.tick()
            self.controller_tick()
            self.sound_controller.crash_sound()
            self.display_manager.black_screen()

    def controller_tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.event_manager.process_event(event.key, hard=True)
        keys = pygame.key.get_pressed()
        if sum(keys):
            for index in range(len(keys)):
                if keys[index]:
                    self.event_manager.process_event(index)

    def view_tick(self):
        self.display_manager.update_display()

    def sound_tick(self):
        self.sound_controller.update_sounds()
