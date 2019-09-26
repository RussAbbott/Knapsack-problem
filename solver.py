"""
The solver manager for the Coursera Dynamic Optimization Knapsack homework.
"""

from collections import namedtuple
from time import process_time
from typing import List

from basic_solvers import dynamic_prog, greedy_by_density
from bb_solver import BBSolver


Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])


def make_Item(index, value, weight):
    """

    :param index: 
    :param value: 
    :param weight: 
    :return: 
    """
    return Item(index, value, weight, value/weight)


def apply_solver(solver, items_count, capacity, density_sorted_items,
                 verbose_outline, verbose_tracking):
    """

    :param solver:
    :param items_count: 
    :param capacity: 
    :param density_sorted_items:
    :param verbose_outline:
    :param verbose_tracking:
    :return:
    """
    print(f'\n{solver.__name__}\n{"".join(["-"]*len(solver.__name__))}')

    start = process_time()
    (value, taken_density_sorted_items) = solver(items_count, capacity, density_sorted_items, verbose_tracking)
    elapsed_time = process_time() - start

    taken_items = sorted(
        [density_sorted_items[dpbb_index].index for dpbb_index in taken_density_sorted_items])
    # All results are optimal except greedy_by_density
    if verbose_outline:
        print(f' -> Elapsed time: {elapsed_time} sec')
        output_data = f'{value} {int(solver is not greedy_by_density)}\n{taken_items}'
        print(output_data)

    return (value, int(solver is not greedy_by_density), taken_items)


def bb_solver(items_count, capacity, density_sorted_items, verbose_tracking):
    """
    Run the bb_solver.
    :param density_sorted_items:
    :param items_count:
    :param capacity: 
    :param verbose_tracking:
    :return:
    """
    return BBSolver(items_count, capacity, density_sorted_items, verbose_tracking)()


def solve_a_dataset(input_data,
                    solvers=(greedy_by_density, bb_solver, dynamic_prog),
                    prob_nbr=None,
                    verbose_outline=False,
                    verbose_tracking=False):
    """
    
    :param input_data:
    :param solvers:
    :param prob_nbr:
    :param verbose_outline:
    :param verbose_tracking:
    :return:
    """
    equals_line = "==" * 50
    lines = input_data.split('\n')
    (items_count, capacity) = map(int, lines[0].split())
    problem_size = round(items_count * capacity / 1E6)  # 1E6 == 1,000,000 == 1 million
    print(f'\n{equals_line}\n{prob_nbr})'
                                      f' {file_location}.    '
                                      f'Problem size (items_count ({items_count}) * capacity ({capacity})):'
                                      f' {problem_size} million\n'
                                      f'{equals_line}')
    # Each result is (value, opt, taken)
    items = [make_Item(i, *map(int, lines[i + 1].split())) for i in range(items_count)]
    density_sorted_items: List[Item] = sorted(items, key=lambda item: item.density, reverse=True)
    if tracking_verbosity:
        print('\nItems')
        for (n, item) in enumerate(items):
            print(f'{n}. {item}')
        print('\nDensity-sorted items')
        for (n, item) in enumerate(density_sorted_items):
            print(f'{n}. {item}')
    results = [apply_solver(solver, items_count, capacity, density_sorted_items,
                            verbose_outline, verbose_tracking)
               for solver in solvers]

    # Select the result with the highest value.
    # If two are tied, select the one with the shortest list of 'taken' items.
    (value, opt, taken_items) = max(results, key=lambda result_item: (result_item[0], -len(result_item[2])))
    taken_string = ' '.join(map(str, [(1 if i in taken_items else 0) for i in range(items_count)]))
    submission = f'{value} {opt}\n{taken_string}'
    print('\nSubmission:')
    return submission


if __name__ == '__main__':
    # Run the program on some data sets.
    for (prob_nbr, file_location) in enumerate(
        # This first empty list lets you add other file names to it.
        []
        # This is the first file in the data folder. It is very small and good for a first test of your solver.
        # The homework sheet has a trace produced by one of the solvers. 
        # + ['./data/ks_4_0']
        
        # These are the data sets the system uses for testing. Add or comment out the ones you want/don't want.
        + ['./data/ks_30_0']
        + ['./data/ks_50_0']
        + ['./data/ks_200_0']
        + ['./data/ks_400_0']
        + ['./data/ks_1000_0']
        + ['./data/ks_10000_0']
        ):
        # Reads/treats the entire file as a single string.
        solvers = (greedy_by_density, bb_solver, dynamic_prog)

        input_data = open(file_location, 'r').read()

        # If True, show the solvers used and the results they achieve
        verbose_outline = True

        # If True, show some of the details of how the solvers run.
        tracking_verbosity = False

        submission = solve_a_dataset(input_data, solvers, prob_nbr+1, verbose_outline, tracking_verbosity)

        # To run this for submission, you will have to get it to work as called by submit.py -- with no
        # additional output.
        print(submission)
