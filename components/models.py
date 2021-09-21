import json

import numpy as np

from components.constants import constants


class Sudoku:
    def __init__(self, size: int = constants.levels[0], json_obj: dict = None):
        self.size = size
        self.grid = np.zeros((size, size))
        self.fixed = None
        self.chosen = None
        self.moves = 0
        self.time_taken_sec = 0
        if json_obj:
            self.size = json_obj.get("size")
            self.grid = json_obj.get("grid")
            self.fixed = json_obj.get("fixed")
            self.chosen = json_obj.get("chosen")
            self.moves = json_obj.get("moves")
            self.time_taken_sec = json_obj.get("time_taken_sec")

    def to_json(self):
        return {
            "size": self.size,
            "grid": self.grid,
            "fixed": self.fixed,
            "chosen": self.chosen,
            "moves": self.moves,
            "time_taken_sec": self.time_taken_sec,
        }

    def cell_size(self):
        return constants.s_side / self.size


class Score:
    def __init__(self, json_obj: dict = None):
        self.wins = 0
        self.surrenders = 0
        self.match = None
        if json_obj:
            self.wins = json_obj.get("wins")
            self.match = json_obj.get("match")

    def to_json(self):
        return {
            "match": json.dumps(self.match.to_json(), indent=2),
            "wins": self.wins,
        }
