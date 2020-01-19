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
        """The main loop iterating as long,  as the game is running"""
        while self.running:
            milliseconds_passed = self.clock.tick()
            self.controller_tick()
            self.zeppelin.update_values(milliseconds_passed)
            if self.zeppelin.crashed:
                self.game_over()
            else:
                self.view_tick()
                self.sound_tick()

    def game_over(self):
        """View the black screen when zeppelin is crashed"""
        while self.running:
            milliseconds_passed = self.clock.tick()
            self.controller_tick()
            self.sound_controller.crash_sound()
            self.display_manager.black_screen()

    def controller_tick(self):
        """Get all events and send them to the event manager"""
        for event in pygame.event.get():
            # Stop the game when quit signal appears
            if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.running = False
            # When a button starts to be pressed, process an event with hard=True
            elif event.type == pygame.KEYDOWN:
                self.event_manager.process_event(event.key, hard=True)

        # Also get all keys that continue to be pressed
        keys = pygame.key.get_pressed()
        if sum(keys):   # if any keys are currently pressed
            # Process an event with hard=False (default)
            for index in range(len(keys)):
                if keys[index]:
                    self.event_manager.process_event(index)

    def view_tick(self):
        self.display_manager.update_display()

    def sound_tick(self):
        self.sound_controller.update_sounds()
