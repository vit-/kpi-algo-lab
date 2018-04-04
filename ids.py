from multiprocessing import Pool
from time import time

from board import Board, random_start_board
from stats import print_stats


class UniqueStack(object):

    def __init__(self):
        self._stack = []
        self._processed = set()

    def __repr__(self):
        return str(self._stack)

    def add(self, item):
        if item not in self._processed:
            self._stack.append(item)
            self._processed.add(item)

    def pop(self):
        return self._stack.pop()

    def has_items(self):
        return bool(self._stack)


def noinf_alg(desired_board):
    stack = UniqueStack()
    stack.add(Board())

    cnt = 0
    trace = []
    solution = None
    start_time = time()
    while stack.has_items():
        cnt += 1
        board = stack.pop()
        if board == desired_board:
            solution = board
            break
        for new_board in board.generate_moves():
            stack.add(new_board)
            trace.append(new_board.zero)
    spent_time = time() - start_time
    stats = {
        'time': spent_time,
        'iterations': cnt,
        'generated_boards': len(stack._processed),
    }
    return solution, stats


def print_trace(board, n=3):
    all_nodes = []
    while board:
        all_nodes.append(board)
        board = board.parent
    if all_nodes:
        for i in all_nodes[:n]:
            print(i)
        print('...truncated...')
        for i in all_nodes[-n:]:
            print(i)


def run(_):
    board = random_start_board()
    return noinf_alg(board)


if __name__ == '__main__':
    N = 20
    with Pool(10) as p:
        results = p.map(run, range(N))
    print_stats(results)
