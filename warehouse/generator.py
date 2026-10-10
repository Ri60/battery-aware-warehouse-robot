import random

from warehouse.grid import Warehouse


def generate_warehouse(
    rows=10,
    cols=10,
    obstacle_density=0.20,
    charger_count=2,
    battery_capacity=10,
    initial_battery=None,
    min_movement_time=1,
    max_movement_time=5,
    seed=None,
    start=None,
    goal=None,
):
    """
    Generate a reproducible randomized warehouse.

    Parameters:
        rows:
            Number of rows in the grid.

        cols:
            Number of columns in the grid.

        obstacle_density:
            Fraction of cells that should become blocked.

        charger_count:
            Number of charging stations.

        battery_capacity:
            Maximum robot battery.

        initial_battery:
            Starting battery. Defaults to full capacity.

        min_movement_time:
            Minimum movement-time edge cost.

        max_movement_time:
            Maximum movement-time edge cost.

        seed:
            Random seed used to reproduce the same warehouse.

        start:
            Optional fixed start position.

        goal:
            Optional fixed goal position.
    """

    if rows < 2 or cols < 2:
        raise ValueError(
            "Warehouse must have at least 2 rows and 2 columns."
        )

    if not 0 <= obstacle_density < 1:
        raise ValueError(
            "Obstacle density must be between 0 and 1."
        )

    if charger_count < 0:
        raise ValueError(
            "Charger count cannot be negative."
        )

    if battery_capacity <= 0:
        raise ValueError(
            "Battery capacity must be greater than zero."
        )

    if min_movement_time <= 0:
        raise ValueError(
            "Minimum movement time must be greater than zero."
        )

    if max_movement_time < min_movement_time:
        raise ValueError(
            "Maximum movement time cannot be less than minimum movement time."
        )

    rng = random.Random(seed)

    all_cells = [
        (row, col)
        for row in range(rows)
        for col in range(cols)
    ]

    # Choose start and goal if they were not provided.
    if start is None:
        start = rng.choice(all_cells)

    if goal is None:
        possible_goals = [
            cell
            for cell in all_cells
            if cell != start
        ]

        goal = rng.choice(possible_goals)

    if start == goal:
        raise ValueError(
            "Start and goal must be different."
        )

    if start not in all_cells:
        raise ValueError(
            "Start position is outside the warehouse."
        )

    if goal not in all_cells:
        raise ValueError(
            "Goal position is outside the warehouse."
        )

    # Cells available for obstacles.
    obstacle_candidates = [
        cell
        for cell in all_cells
        if cell not in {start, goal}
    ]

    obstacle_count = int(
        len(all_cells) * obstacle_density
    )

    obstacle_count = min(
        obstacle_count,
        len(obstacle_candidates),
    )

    blocked_cells = set(
        rng.sample(
            obstacle_candidates,
            obstacle_count,
        )
    )

    # Chargers must be on open cells.
    charger_candidates = [
        cell
        for cell in all_cells
        if cell not in blocked_cells
        and cell not in {start, goal}
    ]

    actual_charger_count = min(
        charger_count,
        len(charger_candidates),
    )

    chargers = set(
        rng.sample(
            charger_candidates,
            actual_charger_count,
        )
    )

    # Generate movement-time costs for every valid adjacent edge.
    edge_costs = {}

    directions = [
        (1, 0),
        (0, 1),
    ]

    for row in range(rows):
        for col in range(cols):
            current = (row, col)

            if current in blocked_cells:
                continue

            for dr, dc in directions:
                neighbor = (
                    row + dr,
                    col + dc,
                )

                neighbor_row, neighbor_col = neighbor

                if not (
                    0 <= neighbor_row < rows
                    and 0 <= neighbor_col < cols
                ):
                    continue

                if neighbor in blocked_cells:
                    continue

                edge_costs[
                    (current, neighbor)
                ] = rng.randint(
                    min_movement_time,
                    max_movement_time,
                )

    if initial_battery is None:
        initial_battery = battery_capacity

    return Warehouse(
        rows=rows,
        cols=cols,
        start=start,
        goal=goal,
        blocked_cells=blocked_cells,
        chargers=chargers,
        edge_costs=edge_costs,
        battery_capacity=battery_capacity,
        initial_battery=initial_battery,
    )