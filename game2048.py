from functools import reduce
import numpy as np
import random


class Board:
    KEY_MAP = {'d': 0, 's': 1, 'a': 2, 'w': 3}

    def __init__(self, n=4, seed=None):
        self.board = np.zeros((n, n), dtype=np.int64)
        self.n = n
        self.score = 0
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        self.generate(True)
        self.generate(True)

    @property
    def done(self):
        return self.board.all()

    def _move_helper(self, board):
        def merge(prev, cur):
            if prev[-1] == cur:
                self.score += cur * 2
                return prev[:-1] + [cur * 2, 0]
            else:
                return prev + [cur]

        new = []
        for row in board:
            merged = reduce(merge, filter(None, row), [0])
            merged = [i for i in merged if i]
            new.append([0] * (self.n - len(merged)) + merged)
        return np.array(new, dtype=self.board.dtype)

    def generate(self, forced=False):
        generated = 2 if random.random() < 0.9 or forced else 4
        loc = random.choice(np.argwhere(self.board == 0))
        self.board[tuple(loc)] = generated

    def move(self, act):  # right=0, down=1, left=2, up=3
        board = np.rot90(self.board, k=act)
        board = self._move_helper(board)
        self.board = np.rot90(board, k=-act)

    def step(self, act):
        act = act if type(act) == int else self.KEY_MAP.get(act, None)
        if act is not None:
            self.move(act)
            self.generate()

    def reset(self):
        self.board = np.zeros((self.n, self.n), dtype=self.board.dtype)

    def __str__(self):
        return str(self.board)

    def __repr__(self):
        return repr(self.board)


if __name__ == '__main__':
    game = Board(4)
    print(game)
    while not game.done:
        game.step(input())
        print('score:', game.score)
        print(game)
