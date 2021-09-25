from pygame.locals import *

from components.methods import *
from components.models import Sudoku, CartesianPoint

pygame.init()


def main(surface: pygame.Surface, level: int):
    game = Sudoku(size=constants.levels[level])
    run = GameState.running
    clock = pygame.time.Clock()
    game_time = 0
    pause_time = 0
    point = CartesianPoint((0, 0))
    while run != GameState.over:
        clock.tick()
        if run != GameState.running:
            pause_time += clock.get_rawtime()
        game_time += clock.get_rawtime()
        game.time_taken_sec = (game_time - pause_time) // 1000
        draw_game_window(surface, game, point, run == GameState.running)

        for event in pygame.event.get():
            if event.type == QUIT:
                if run == GameState.running:
                    run = GameState.paused
                else:
                    run = GameState.over
            elif event.type == KEYDOWN:
                if run == GameState.running:
                    if event.key == K_DOWN:
                        point.y = (point.y + 1) % game.size
                    elif event.key == K_UP:
                        point.y = (point.y - 1) % game.size
                    elif event.key == K_LEFT:
                        point.x = (point.x - 1) % game.size
                    elif event.key == K_RIGHT:
                        point.x = (point.x + 1) % game.size
                    elif K_1 <= event.key <= (K_1 + game.size - 1):
                        # upper numbers
                        game.update(point, event.key - K_1 + 1)
                    elif K_KP1 <= event.key <= (K_KP1 + game.size - 1):
                        # numpad keys
                        game.update(point, event.key - K_KP1 + 1)
                    elif event.key in constants.exit_pause_keys:
                        run = GameState.paused
                else:
                    if event.key in constants.exit_pause_keys:
                        run = GameState.over
                    elif event.key in constants.continue_keys:
                        run = GameState.running


def main_menu(surface: pygame.Surface):
    run = True
    level = 0
    while run:
        draw_menu_window(surface, level)

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    level = (level + 1) % len(constants.levels)
                elif event.key == K_UP:
                    level = (level - 1) % len(constants.levels)
                elif event.key in constants.exit_pause_keys:
                    run = False
                elif event.key in constants.continue_keys:
                    main(surface, level)

    pygame.display.quit()


if __name__ == "__main__":
    window = pygame.display.set_mode(constants.play_area)
    pygame.display.set_caption(constants.app_name)
    main_menu(window)
