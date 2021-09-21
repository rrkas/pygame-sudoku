import pygame
from pygame.locals import *

pygame.font.init()


class Constants:
    def __init__(self):
        # strings
        self.app_name = "Sudoku"

        # dimensions
        self.levels = [3, 4, 9, 16, 25]

        self.s_side = 500
        self.padding = 10

        self.app_name_fontsize = 50
        self.level_fontsize = 35

        self.timer_fontsize = 20

        self.play_area = (
            self.s_side + 2 * self.padding,
            self.s_side
            + 3 * self.padding
            + self.app_name_fontsize
            + self.level_fontsize
            + self.timer_fontsize,
        )

        self.top_left_x = self.padding
        self.top_left_y = self.padding + self.app_name_fontsize + self.level_fontsize

        # colors
        self.color_bg = (128, 128, 128, 128)
        self.color_grid = (0, 0, 0)
        self.color_cell = (255, 255, 255)
        self.color_fixed = (0, 0, 0)
        self.color_picked_accepted = (0, 255, 0)
        self.color_picked_error = (255, 0, 0)

        self.color_level_default = (255, 255, 255)
        self.color_level_selected = (255, 255, 0)
        self.color_label = (0, 0, 0)

        # fonts
        self.font_global = "comicsans"

        # keys
        self.continue_keys = [K_KP_ENTER, K_RETURN]
        self.exit_pause_keys = [K_ESCAPE]


constants = Constants()
