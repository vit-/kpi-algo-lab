from collections import defaultdict
from math import inf
from multiprocessing import Pool
from queue import PriorityQueue
from time import time

from board import Board, random_start_board
from stats import print_stats

# https://en.wikipedia.org/wiki/A*_search_algorithm

TIME_LIMIT_SEC = 60


def heuristic_cost_estimate(start, end):
    cost = 0
    for i, line in enumerate(start._state):
        for j, item in enumerate(line):
            if item != end._state[i][j]:
                cost += 1
    return cost


def reconstruct_path(came_from, node):
    total_path = [node]
    while node in came_from:
        node = came_from[node]
        total_path.append(node)
    return total_path


def dist_between(start, end):
    return 1


def astar(desired_board):
    empty_board = Board()

    closed_set = set()
    open_items = PriorityQueue()
    f_score = heuristic_cost_estimate(empty_board, desired_board)
    open_items.put((f_score, empty_board))
    came_from = {}

    g_score = defaultdict(lambda: inf)
    g_score[empty_board] = 0

    cnt = 0
    start_time = time()

    def get_stats():
        return {
            'time': time() - start_time,
            'iterations': cnt,
            'generated_boards': len(closed_set),
        }

    while not open_items.empty():
        if time() - start_time > TIME_LIMIT_SEC:
            return None, get_stats()
        cnt += 1

        _, current = open_items.get()
        if current == desired_board:
            result = reconstruct_path(came_from, current)
            return result[0], get_stats()

        closed_set.add(current)

        for new_board in current.generate_moves():
            if new_board in closed_set:
                continue

            tentative_g_score = g_score[current] + dist_between(current, new_board)
            if tentative_g_score >= g_score[new_board]:
                continue

            came_from[new_board] = current
            g_score[new_board] = tentative_g_score

            f_score = tentative_g_score + heuristic_cost_estimate(new_board, desired_board)
            open_items.put((f_score, new_board))


def run(_):
    board = random_start_board()
    return astar(board)


if __name__ == '__main__':
    N = 20
    with Pool(10) as p:
        results = p.map(run, range(N))
    print_stats(results)
