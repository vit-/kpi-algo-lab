from random import choice


def randomize(board, iterations=100):
    for _ in range(iterations):
        board = choice(list(board.generate_moves()))
    return board


def random_start_board():
    return randomize(Board())


class Board(object):
    n = 3
    m = 3

    moves = [
        # dx, dy
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    def __init__(self, state=None, parent=None):
        self.parent = parent
        if state:
            self._state = tuple(tuple(i) for i in state)
        else:
            choices = list(range(self.n * self.m))
            self._state = tuple(
                tuple(choices.pop() for _ in range(self.n)) for __ in range(self.m)
            )
        for i in range(self.n):
            for j in range(self.m):
                if self._state[i][j] == 0:
                    self.zero = (i, j)

    def __eq__(self, other):
        return self._state == other._state

    def __gt__(self, other):
        return False

    def __hash__(self):
        return hash(self._state)

    def __repr__(self):
        res = ''
        for line in self._state:
            for item in line:
                res += '%s ' % item
            res += '\n'
        return res

    @property
    def state(self):
        return list(list(i) for i in self._state)

    def generate_moves(self):
        x, y = self.zero
        for dx, dy in self.moves:
            new_x = x + dx
            new_y = y + dy
            if self.is_move_valid(new_x, new_y):
                yield self.new_board(new_x, new_y)

    def is_move_valid(self, new_x, new_y):
        return -1 < new_x < self.n and -1 < new_y < self.m

    def new_board(self, new_x, new_y):
        x, y = self.zero
        state = self.state
        tmp = state[new_x][new_y]
        state[new_x][new_y] = 0
        state[x][y] = tmp
        return self.__class__(state=state)  # , parent=self)
