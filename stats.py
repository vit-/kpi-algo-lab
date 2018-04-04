from collections import defaultdict
from prettytable import PrettyTable


def print_stats(results):
    table = PrettyTable(['Start board', 'time', 'iterations', 'Generated boards'])
    totals = defaultdict(int)
    for solution, stats in results:
        for key, value in stats.items():
            totals[key] += value
        table.add_row(
            [str(solution), stats['time'], stats['iterations'], stats['generated_boards']])
    cnt = len(results)
    table.add_row(['*Totals*', totals['time'], totals['iterations'], totals['generated_boards']])
    for key, value in totals.items():
        totals[key] = totals[key] / cnt
    table.add_row(['*Avg*', totals['time'], totals['iterations'], totals['generated_boards']])
    print(table)
