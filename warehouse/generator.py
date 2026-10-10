import random
from collections import deque

from warehouse.grid import Warehouse


def has_battery_feasible_route(warehouse):
    """
    Check whether at least one route can reach the goal
    without violating the battery constraint.

    This is only used to validate generated maps.
    It is NOT one of the search algorithms being evaluated.
    """

    start_state = (
        warehouse.start[0],
        warehouse.start[1],
        warehouse.initial_battery,
    )

    frontier = deque([start_state])
    visited = {start_state}

    while frontier:
        row, col, battery = frontier.popleft()

        if (row, col) == warehouse.goal:
            return True

        # Recharge when standing on a charger.
        if (
            warehouse.is_charger(row, col)
            and battery < warehouse.battery_capacity
        ):
            recharge_state = (
                row,
                col,
                warehouse.battery_capacity,
            )

            if recharge_state not in visited:
                visited.add(recharge_state)
                frontier.append(recharge_state)

        # Movement requires at least one battery unit.
        if battery <= 0:
            continue

        new_battery = warehouse.battery_after_move(battery)

        if new_battery is None:
            continue

        for neighbor in warehouse.get_neighbors(row, col):
            next_state = (
                neighbor[0],
                neighbor[1],
                new_battery,
            )

            if next_state not in visited:
                visited.add(next_state)
                frontier.append(next_state)

    return False


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
    ensure_solution=False,
    max_attempts=200,
):
    """
    Generate a reproducible randomized warehouse.

    ensure_solution=False:
        The generated instance may be solvable or unsolvable.

    ensure_solution=True:
        Regenerate obstacles, chargers, and edge costs until
        a battery-feasible route exists.

    The same seed and parameters always produce the same result.
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

    if max_attempts <= 0:
        raise ValueError(
            "Maximum attempts must be greater than zero."
        )

    if initial_battery is None:
        initial_battery = battery_capacity

    if not 0 <= initial_battery <= battery_capacity:
        raise ValueError(
            "Initial battery must be between 0 and battery capacity."
        )

    rng = random.Random(seed)

    all_cells = [
        (row, col)
        for row in range(rows)
        for col in range(cols)
    ]

    # Pick start and goal once.
    # Retrying generation should not silently change them.
    if start is None:
        start = rng.choice(all_cells)

    if start not in all_cells:
        raise ValueError(
            "Start position is outside the warehouse."
        )

    if goal is None:
        goal_candidates = [
            cell
            for cell in all_cells
            if cell != start
        ]

        goal = rng.choice(goal_candidates)

    if goal not in all_cells:
        raise ValueError(
            "Goal position is outside the warehouse."
        )

    if start == goal:
        raise ValueError(
            "Start and goal must be different."
        )

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

    number_of_open_non_special_cells = (
        len(all_cells)
        - 2
        - obstacle_count
    )

    if charger_count > number_of_open_non_special_cells:
        raise ValueError(
            "Requested charger count is too large "
            "for the selected map and obstacle density."
        )

    for _ in range(max_attempts):
        blocked_cells = set(
            rng.sample(
                obstacle_candidates,
                obstacle_count,
            )
        )

        charger_candidates = [
            cell
            for cell in all_cells
            if cell not in blocked_cells
            and cell not in {start, goal}
        ]

        chargers = set(
            rng.sample(
                charger_candidates,
                charger_count,
            )
        )

        edge_costs = {}

        # Only create each undirected edge once.
        directions = [
            (1, 0),   # down
            (0, 1),   # right
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

                    edge_costs[(current, neighbor)] = rng.randint(
                        min_movement_time,
                        max_movement_time,
                    )

        warehouse = Warehouse(
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

        if not ensure_solution:
            return warehouse

        if has_battery_feasible_route(warehouse):
            return warehouse

    raise RuntimeError(
        "Could not generate a battery-feasible warehouse "
        f"after {max_attempts} attempts. "
        "Try reducing obstacle density, increasing battery capacity, "
        "or adding chargers."
    )