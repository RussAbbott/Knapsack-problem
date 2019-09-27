"""
The solver manager for the Coursera Dynamic Optimization Knapsack homework.
"""

from collections import namedtuple
from time import process_time
from typing import List

from basic_solvers import dynamic_prog, greedy_by_density
from bb_solver import bb_solver


Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])


def apply_solver(solver, items_count, capacity, items_sorted_density,
                 verbose_outline, verbose_tracking):
    """

    :param solver:
    :param items_count: 
    :param capacity: 
    :param items_sorted_density:
    :param verbose_outline:
    :param verbose_tracking:
    :return:
    """
    if verbose_outline:
        print(f'\n{solver.__name__}\n{"".join(["-"]*len(solver.__name__))}')

    start = process_time()
    (value, taken_items_sorted_by_density) = solver(items_count, capacity, items_sorted_density, verbose_tracking)
    elapsed_time = round(process_time() - start, 2)

    # Convert the taken items from using the sorted_items indices to using the original indices.
    # Then sort those indices.
    taken_items = sorted([items_sorted_density[dpbb_index].index for dpbb_index in taken_items_sorted_by_density])
    # All results are optimal except greedy_by_density
    is_optimal = int(solver is not greedy_by_density)
    if verbose_outline:
        print(f' -> Elapsed time: {elapsed_time} sec')
        output_data = f'{value} {is_optimal}\n{taken_items}'
        print(output_data)

    return (value, is_optimal, taken_items)


def make_an_Item(index, value, weight):
    """

    :param index:
    :param value:
    :param weight:
    :return:
    """
    return Item(index=index, value=value, weight=weight, density=value/weight)


def solve_a_dataset(input_data,
                    solvers=(greedy_by_density, bb_solver, dynamic_prog),
                    prob_nbr=None,
                    verbose_outline=False,
                    verbose_tracking=False):
    """
    Run the indicated solvers on the input_data dataset.
    Select the best result.    
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
    items = [make_an_Item(i, *map(int, lines[i + 1].split())) for i in range(items_count)]
    items_sorted_density: List[Item] = sorted(items, key=lambda item: item.density, reverse=True)
    if tracking_verbosity:
        print('\nItems')
        for (n, item) in enumerate(items):
            print(f'{n}. {item}')
        print('\nDensity-sorted items')
        for (n, item) in enumerate(items_sorted_density):
            print(f'{n}. {item}')
    results = [apply_solver(solver, items_count, capacity, items_sorted_density,
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
        # This empty list lets you add other file names to it.
        []
        # This is the first file in the data folder. It is very small and good for a first test of your solver.
        # The homework sheet has a trace produced by an earlier version of the bb_solver.
        #      Timings in seconds:    bb          dp
        # + ['./data/ks_4_0']         # 0.0         0.0
        # + ['./data/ks_6_0']         # 0.0         0.0

        # These are the data sets the system uses for testing. Add or comment out the ones you want/don't want to try.
        # Coursera numbers these data sets 1 - 6.
        #                                           Problem size    Time in seconds
        #                               Solution    in millions      bb   bb+gbd         dp
        # + ['./data/ks_30_0']       #    99798          3          0.11   0.12         3.42
        # + ['./data/ks_50_0']       #   142156         17          0.02   0.00        19.7
        # + ['./data/ks_200_0']      #   100236         20          0.75   0.56        19.62
        # + ['./data/ks_400_0']      #  3967180       3795          2.75   3.36      4335.46 =  72.26 min
        # + ['./data/ks_1000_0']     #   109899        100          0.41   0.48       119.01 =   1.98 min
        + ['./data/ks_10000_0']    #  1099893      10000          4.46   4.78     13170.43 = 219.51 min = 3.66 hours
        ):

        solvers = (bb_solver, )  #(greedy_by_density, bb_solver, dynamic_prog)

        # Reads/treats the entire file as a single string.
        input_data = open(file_location, 'r').read()

        # If True, show the solvers used and the results they achieve
        verbose_outline = True

        # If True, show some of the details of how the solvers run.
        tracking_verbosity = False

        submission = solve_a_dataset(input_data, solvers, prob_nbr, verbose_outline, tracking_verbosity)

        # To run this for submission, you will have to get it to work as called by submit.py -- with no
        # additional output.
        print(submission)
