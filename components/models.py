import json
import random
from typing import List, Union

import numpy as np


class CartesianPoint:
    def __init__(self, xy: tuple = (0, 0)):
        self.x = xy[0]
        self.y = xy[1]

    def to_tuple(self):
        return self.x, self.y

    def __repr__(self):
        return "repr:" + str((self.x, self.y))

    def __str__(self):
        return "str:" + str((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, tuple):
            return (self.x, self.y) == other
        else:
            return False


class Data:
    def __init__(self):
        try:
            with open("data.json") as f:
                json_data = json.load(f)
                for k, grids in json_data.items():
                    l = []
                    for grid in grids:
                        t = []
                        for row in grid:
                            t.append(list(map(int, row.split())))
                        t = np.array(t)
                        l.append(t)
                    self.__setattr__(f"{k}x{k}", l)
        except BaseException as e:
            print(e)


from components.constants import constants


class Sudoku:
    def __init__(self, size: int = constants.levels[0], json_obj: dict = None):
        self.size = size
        self.grid: np.ndarray = random.sample(
            constants.data.__getattribute__(f"{size}x{size}"), 1
        )[0]
        self.fixed: List[CartesianPoint] = []
        for i, j in np.argwhere(self.grid != 0):
            self.fixed.append(CartesianPoint((i, j)))
        self.chosen_err: List[CartesianPoint] = []
        self.moves: int = 0
        self.time_taken_sec: int = 0
        if json_obj:
            self.size = json_obj.get("size")
            self.grid = np.ndarray(json_obj.get("grid"))
            self.fixed = [CartesianPoint(xy=f) for f in json_obj.get("fixed")]
            self.moves = json_obj.get("moves")
            self.time_taken_sec = json_obj.get("time_taken_sec")

    def to_json(self):
        return {
            "size": self.size,
            "grid": self.grid.tolist(),
            "fixed": [f.to_tuple() for f in self.fixed],
            "moves": self.moves,
            "time_taken_sec": self.time_taken_sec,
        }

    def cell_size(self):
        return constants.s_side / self.size

    def valid_cell(self, point: Union[CartesianPoint, tuple]):
        return point not in self.fixed

    def update(self, point: CartesianPoint, value: int):
        # x,y = j,i
        if self.valid_cell((point.y, point.x)):
            self.grid[point.y][point.x] = value
        self.get_invalid_chosen()

    def get_invalid_chosen(self):
        self.chosen_err = []
        for i in range(self.size):
            r = self.grid[i, :].tolist()
            c = self.grid[:, i].tolist()
            for j in range(self.size):
                e = r[j]
                if e > 0 and r.count(e) > 1:
                    if (i, j) not in self.fixed and (i, j) not in self.chosen_err:
                        self.chosen_err.append(CartesianPoint((i, j)))
                e = c[j]
                if e > 0 and c.count(e) > 1:
                    if (j, i) not in self.fixed and (j, i) not in self.chosen_err:
                        self.chosen_err.append(CartesianPoint((j, i)))


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


class GameState:
    running = 1
    paused = 2
    over = 3
