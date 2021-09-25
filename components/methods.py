import pygame
from pygame import Surface

from components.models import *

print()

from components.constants import constants


def level_menu(surface: pygame.Surface, level: int):
    start_top = 3 * constants.padding + 2 * constants.app_name_fontsize
    for i, l in enumerate(constants.levels):
        draw_text_middle(
            surface,
            f"{l}x{l}",
            constants.app_name_fontsize,
            constants.color_level_selected
            if i == level
            else constants.color_level_default,
            margin_top=start_top + i * constants.app_name_fontsize,
        )


def draw_grid(surface: pygame.Surface, game: Sudoku, point: CartesianPoint):
    num_font = pygame.font.SysFont(
        constants.monospace,
        int(game.cell_size() / 2),
        bold=True,
    )
    for i in range(game.size):
        for j in range(game.size):
            rect_x = (
                constants.top_left_x
                + j * game.cell_size()
                + constants.border_grid_width
            )
            rect_y = (
                constants.top_left_y
                + i * game.cell_size()
                + constants.border_grid_width
            )
            rect_size = game.cell_size() - constants.border_grid_width / 2
            if (i, j) in game.fixed:
                pygame.draw.rect(
                    surface,
                    constants.color_fixed_bg,
                    pygame.Rect(rect_x, rect_y, rect_size, rect_size),
                )
            elif (i, j) in game.chosen_err:
                pygame.draw.rect(
                    surface,
                    constants.color_chosen_num_err,
                    pygame.Rect(rect_x, rect_y, rect_size, rect_size),
                )
            num_surface = num_font.render(
                str(game.grid[i][j]) if game.grid[i][j] != 0 else "",
                True,
                constants.color_fixed_num
                if (i, j) in game.fixed
                else constants.color_cell_bg
                if (i, j) in game.fixed
                else constants.color_chosen_num,
            )
            num_rect = num_surface.get_rect(
                center=(rect_x + rect_size / 2, rect_y + rect_size / 2)
            )
            surface.blit(num_surface, num_rect)
        pygame.draw.line(
            surface,
            constants.color_grid,
            (constants.top_left_x + i * game.cell_size(), constants.top_left_y),
            (
                constants.top_left_x + i * game.cell_size(),
                constants.top_left_y + constants.s_side,
            ),
            constants.border_grid_width,
        )
        pygame.draw.line(
            surface,
            constants.color_grid,
            (constants.top_left_x, constants.top_left_y + i * game.cell_size()),
            (
                constants.top_left_x + constants.s_side,
                constants.top_left_y + i * game.cell_size(),
            ),
            constants.border_grid_width,
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
        width=constants.border_grid_width,
    )
    pygame.draw.rect(
        surface,
        constants.color_chosen_num,
        pygame.Rect(
            constants.top_left_x
            + point.x * game.cell_size()
            + constants.border_grid_width,
            constants.top_left_y
            + point.y * game.cell_size()
            + constants.border_grid_width,
            game.cell_size() - constants.border_grid_width,
            game.cell_size() - constants.border_grid_width,
        ),
        width=2 * constants.border_grid_width,
    )


def draw_paused_message(surface: pygame.Surface):
    height_overlap = 100
    rect = pygame.Rect(
        constants.top_left_x + 2 * constants.padding,
        constants.top_left_y + (constants.s_side - height_overlap) / 2,
        constants.s_side - 4 * constants.padding,
        height_overlap,
    )
    pygame.draw.rect(surface, constants.color_overlap_bg, rect)

    font = pygame.font.SysFont(
        constants.monospace,
        constants.level_fontsize,
        bold=True,
    )
    paused_surface = font.render("Paused", 1, constants.color_grid)
    paused_rect = paused_surface.get_rect(center=rect.center)
    surface.blit(paused_surface, paused_rect)


def draw_game_window(
    surface: pygame.Surface, game: Sudoku, point: CartesianPoint, running: bool
):
    surface.fill(constants.color_bg)
    surface.fill(
        constants.color_cell_bg,
        rect=pygame.Rect(
            constants.top_left_x,
            constants.top_left_y,
            constants.s_side,
            constants.s_side,
        ),
    )
    hour, minute, sec = (
        game.time_taken_sec // 3600,
        (game.time_taken_sec // 60) % 60,
        game.time_taken_sec % 60,
    )

    if hour:
        game_time = f"{str(hour).zfill(2)}:{str(minute).zfill(2)}:{str(sec).zfill(2)}"
    else:
        game_time = f"{str(minute).zfill(2)}:{str(sec).zfill(2)}"
    draw_text_middle(
        surface,
        constants.app_name,
        constants.app_name_fontsize,
        constants.color_label,
        margin_top=constants.padding + constants.level_fontsize / 2,
    )
    draw_text_middle(
        surface,
        game_time,
        constants.level_fontsize,
        constants.color_label,
        margin_top=constants.play_area[1]
        - constants.level_fontsize
        - constants.padding // 2,
        monospace=True,
    )
    draw_grid(surface, game, point)
    if not running:
        draw_paused_message(surface)
    pygame.display.update()


def draw_menu_window(surface: pygame.Surface, level: int):
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


def draw_text_middle(
    surface: Surface, text: str, size: int, color: tuple, margin_top=0, monospace=False
):
    font = pygame.font.SysFont(
        constants.monospace if monospace else constants.font_global, size, bold=True
    )
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


def get_score(level: int = 0) -> Score:
    score = None
    try:
        with open("score.json", "r") as f:
            score = f.read()
            if len(score) > 0:
                score = Score(json_obj=json.loads(score))
            else:
                score = Score(level=level)
    except BaseException as e:
        print(e)
        score = Score(level=level)
    score.game.get_invalid_chosen()
    return score


def set_score(game: Sudoku, surrender: bool = False):
    score = get_score()
    if surrender:
        score.surrenders += 1
        score.game = None
    elif game.is_win():
        score.wins += 1
        score.game = None
    else:
        score.game = game

    with open("score.json", "w") as f:
        f.write(score.to_json())
