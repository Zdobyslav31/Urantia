import pygame

from game import Game

CAPTION = "Urantia"


def main():
    pygame.init()
    pygame.display.set_caption(CAPTION)
    game = Game()
    game.run()
    pygame.quit()


if __name__ == "__main__":
    main()
