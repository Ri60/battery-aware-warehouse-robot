def manhattan_distance(position, goal):
    row1, col1 = position
    row2, col2 = goal

    return abs(row1 - row2) + abs(col1 - col2)


def minimum_movement_time(warehouse):
    if not warehouse.edge_costs:
        return 1

    return min(warehouse.edge_costs.values())


def primary_heuristic(state, warehouse):
    """
    h(n) = Manhattan distance to goal
           x minimum movement-time cost.

    This ignores:
    - walls
    - battery limits
    - charging delays

    So it estimates a lower bound on remaining travel time.
    """

    distance = manhattan_distance(
        state.position,
        warehouse.goal,
    )

    min_cost = minimum_movement_time(warehouse)

    return distance * min_cost