from warehouse.grid import Warehouse


def small_test_map():
    edge_costs = {
        ((0, 0), (0, 1)): 2,
        ((0, 1), (0, 2)): 4,
        ((0, 2), (0, 3)): 1,

        ((0, 0), (1, 0)): 3,
        ((1, 0), (2, 0)): 2,

        ((2, 0), (2, 1)): 1,
        ((2, 1), (2, 2)): 2,
        ((2, 2), (2, 3)): 1,
    }

    return Warehouse(
        rows=3,
        cols=4,
        start=(0, 0),
        goal=(0, 3),
        blocked_cells={
            (1, 1),
            (1, 2),
            (1, 3),
        },
        chargers={
            (2, 1),
        },
        edge_costs=edge_costs,
        battery_capacity=4,
        initial_battery=4,
    )


def charging_required_map():
    return Warehouse(
        rows=2,
        cols=5,
        start=(0, 0),
        goal=(0, 4),
        blocked_cells={
            (1, 2),
            (1, 3),
            (1, 4),
        },
        chargers={
            (1, 1),
        },
        battery_capacity=4,
        initial_battery=3,
    )