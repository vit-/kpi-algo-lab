from collections import defaultdict
from math import inf
from multiprocessing import Pool
from time import time

from board import Board, random_start_board
from stats import print_stats

# https://en.wikipedia.org/wiki/A*_search_algorithm

TIME_LIMIT_SEC = 60


def flatify_state(state):
    res = []
    for line in state:
        for i in line:
            res.append(i)
    return res


def heuristic_cost_estimate(start, end):
    start_state = flatify_state(start.state)
    end_state = flatify_state(end.state)

    cost = 0
    for i in range(len(start_state)):
        if start_state[i] != end_state[i]:
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
    open_set = {empty_board}
    came_from = {}

    g_score = defaultdict(lambda: inf)
    g_score[empty_board] = 0

    f_score = defaultdict(lambda: inf)
    f_score[empty_board] = heuristic_cost_estimate(empty_board, desired_board)

    cnt = 0
    start_time = time()

    def get_cheapest_open_node():
        cheapest = None
        min_cost = None
        for node in open_set:
            cost = f_score[node]
            if min_cost is None or min_cost > cost:
                min_cost = cost
                cheapest = node
        return cheapest

    def get_stats():
        return {
            'time': time() - start_time,
            'iterations': cnt,
            'generated_boards': len(closed_set),
        }

    while open_set:
        if time() - start_time > TIME_LIMIT_SEC:
            return None, get_stats()

        current = get_cheapest_open_node()
        if current == desired_board:
            result = reconstruct_path(came_from, current)
            return result[0], get_stats()

        open_set.remove(current)
        closed_set.add(current)

        for new_board in current.generate_moves():
            if new_board in closed_set:
                continue
            open_set.add(new_board)

            tentative_g_score = g_score[current] + dist_between(current, new_board)
            if tentative_g_score >= g_score[new_board]:
                continue

            came_from[new_board] = current
            g_score[new_board] = tentative_g_score
            f_score[new_board] = (
                g_score[new_board] + heuristic_cost_estimate(new_board, desired_board)
            )


def run(_):
    board = random_start_board()
    return astar(board)


if __name__ == '__main__':
    N = 20
    with Pool(10) as p:
        results = p.map(run, range(N))
    print_stats(results)
