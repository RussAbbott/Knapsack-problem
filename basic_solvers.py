"""
Basic knapsack solvers: dynamic programming and various greedy solvers
"""

from copy import copy


def dynamic_prog(items_count, capacity, density_sorted_items, verbose_tracking):
    """
    Run the dynamic programming algorithm. It is right here!
    :param items_count:
    :param capacity:
    :param density_sorted_items:
    :param verbose_tracking
    :return:
    """
    # Keep only the current and most recent prev column.
    # Each column stores a tuple at each position: (val, list_of_taken_elements)
    col = [(0, [])]*(capacity+1)
    cur = col

    for i in range(items_count):
        pred = cur
        cur = copy(col)
        (index, value, weight, density) = density_sorted_items[i]
        for w in range(capacity+1):
            (p_val, p_elmts) = pred[w - weight] if weight <= w else (0, [])
            cur[w] = max(pred[w], (int(weight <= w) * (value + p_val), p_elmts + [i]),
                         key=lambda valElmts: valElmts[0])
        if verbose_tracking and items_count >= 1000:
            if i > 0 and i % 100 == 0:
                print(f'{i}/{items_count}', end=' ')
                if i % 1000 == 0:
                    print()
    if verbose_tracking and items_count >= 1000:
        print()

    return cur[capacity]


def greedy_by_density(_items_count, capacity, items, _verbose_tracking):
    """
    Run the greedy-by-density algorithm.
    :param _items_count:
    :param capacity:
    :param items:
    :param _verbose_tracking:
    :return:
    """
    return greedy_by_order(capacity, sorted(items, key=lambda item: item.density, reverse=True))


def greedy_by_order(capacity, items):
    """

    :param capacity:
    :param items:
    :return:
    """
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken_greedy = []
    for (index, item) in enumerate(items):
        if weight + item.weight <= capacity:
            taken_greedy.append(index)
            value += item.value
            weight += item.weight
    return (value, sorted(taken_greedy))


def greedy_by_value(_items_count, capacity, items):
    """
    Run the greedy-by-value algorithm.
    :param _items_count:
    :param capacity:
    :param items:
    :return:
    """
    return greedy_by_order(capacity, sorted(items, key=lambda item: item.value, reverse=True))


def greedy_by_weight(_items_count, capacity, items):
    """
    Run the greedy-by-weight algorithm.
    :param _items_count:
    :param capacity:
    :param items:
    :return:
    """
    return greedy_by_order(capacity, sorted(items, key=lambda item: item.weight))
