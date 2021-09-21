import json

import pygame
from pygame import Surface

from components.constants import constants
from components.models import Score, Sudoku


def level_menu(surface: pygame.Surface, level: int):
    start_top = 3 * constants.padding + 2 * constants.app_name_fontsize
    for i, l in enumerate(constants.levels):
        draw_text_middle(
            surface,
            str(l),
            constants.app_name_fontsize,
            constants.color_level_selected
            if i == level
            else constants.color_level_default,
            margin_top=start_top + i * constants.app_name_fontsize,
        )


def draw_grid(surface: pygame.Surface, game: Sudoku):
    for i in range(game.size):
        pygame.draw.line(
            surface,
            constants.color_grid,
            (constants.top_left_x + i * game.cell_size(), constants.top_left_y),
            (
                constants.top_left_x + i * game.cell_size(),
                constants.top_left_y + constants.s_side,
            ),
            1,
        )
        pygame.draw.line(
            surface,
            constants.color_grid,
            (constants.top_left_x, constants.top_left_y + i * game.cell_size()),
            (
                constants.top_left_x + constants.s_side,
                constants.top_left_y + i * game.cell_size(),
            ),
            1,
        )

    pygame.draw.rect(
        surface,
        constants.color_grid,
        pygame.Rect(
            constants.top_left_x,
            constants.top_left_y,
            constants.s_side,
            constants.s_side,
        ),
        width=1,
    )
    pygame.display.update()


def draw_text_middle(
    surface: Surface,
    text: str,
    size: int,
    color: tuple,
    margin_top=0,
):
    font = pygame.font.SysFont(constants.font_global, size, bold=True)
    label = font.render(text, 1, color)

    if margin_top == 0:
        surface.blit(
            label,
            (
                constants.top_left_x
                + constants.play_area[0] / 2
                - (label.get_width() / 2),
                constants.play_area[1] / 2 - (label.get_height() / 2),
            ),
        )
    else:
        surface.blit(
            label,
            (
                constants.top_left_x
                + constants.play_area[0] / 2
                - (label.get_width() / 2),
                margin_top,
            ),
        )


def get_score() -> Score:
    try:
        with open("score.txt", "r") as f:
            score = f.readline()
            if len(score) > 0:
                return Score(json_obj=json.loads(score))
            else:
                return Score()
    except BaseException as e:
        print(e)
        return Score()


def set_score(score: Score):
    try:
        with open("score.txt", "w") as f:
            f.write(json.dumps(score.to_json(), indent=2))
    except BaseException as e:
        print(e)
