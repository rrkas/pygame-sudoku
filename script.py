from pygame.locals import *

from components.methods import *
from components.models import Sudoku

pygame.init()


def main(surface: pygame.Surface, level: int):
    game = Sudoku(size=constants.levels[level])
    run = True
    clock = pygame.time.Clock()
    game_time = 0
    while run:
        game_time += clock.get_rawtime()
        if game_time % 1000 == 0:
            game.time_taken_sec += 1
        surface.fill(constants.color_bg)
        draw_text_middle(
            surface,
            constants.app_name,
            constants.app_name_fontsize,
            constants.color_label,
            margin_top=constants.padding,
        )
        draw_text_middle(
            surface,
            f"{game.time_taken_sec} secs",
            constants.level_fontsize,
            constants.color_label,
            margin_top=constants.play_area[1] - constants.level_fontsize,
        )
        draw_grid(surface, game)

        pygame.display.update()

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

        clock.tick()


def main_menu(surface: pygame.Surface):
    run = True
    level = 0
    while run:
        surface.fill(constants.color_bg)
        draw_text_middle(
            surface,
            constants.app_name,
            constants.app_name_fontsize,
            constants.color_label,
            constants.padding,
        )
        draw_text_middle(
            surface,
            "Choose Level",
            constants.level_fontsize,
            constants.color_label,
            2 * constants.padding + constants.app_name_fontsize,
        )
        level_menu(surface, level)
        draw_text_middle(
            surface,
            "Press enter to play!",
            constants.level_fontsize,
            constants.color_label,
            4 * constants.padding
            + 2 * constants.app_name_fontsize
            + len(constants.levels) * constants.app_name_fontsize,
        )
        pygame.display.update()

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
