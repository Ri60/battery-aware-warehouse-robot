from warehouse.generator import (
    generate_warehouse,
    has_battery_feasible_route,
)


def test_generator_dimensions():
    warehouse = generate_warehouse(
        rows=8,
        cols=6,
        seed=1,
    )

    assert warehouse.rows == 8
    assert warehouse.cols == 6


def test_generator_seed_is_reproducible():
    warehouse1 = generate_warehouse(
        rows=8,
        cols=8,
        obstacle_density=0.20,
        charger_count=2,
        seed=42,
    )

    warehouse2 = generate_warehouse(
        rows=8,
        cols=8,
        obstacle_density=0.20,
        charger_count=2,
        seed=42,
    )

    assert warehouse1.start == warehouse2.start
    assert warehouse1.goal == warehouse2.goal

    assert (
        warehouse1.blocked_cells
        == warehouse2.blocked_cells
    )

    assert (
        warehouse1.chargers
        == warehouse2.chargers
    )

    assert (
        warehouse1.edge_costs
        == warehouse2.edge_costs
    )


def test_start_and_goal_are_open():
    warehouse = generate_warehouse(
        rows=10,
        cols=10,
        obstacle_density=0.30,
        seed=7,
    )

    assert warehouse.start not in warehouse.blocked_cells
    assert warehouse.goal not in warehouse.blocked_cells
    assert warehouse.start != warehouse.goal


def test_exact_charger_count():
    warehouse = generate_warehouse(
        rows=10,
        cols=10,
        obstacle_density=0.20,
        charger_count=4,
        seed=10,
    )

    assert len(warehouse.chargers) == 4


def test_chargers_are_open():
    warehouse = generate_warehouse(
        rows=10,
        cols=10,
        obstacle_density=0.25,
        charger_count=4,
        seed=10,
    )

    for charger in warehouse.chargers:
        assert charger not in warehouse.blocked_cells

        assert charger != warehouse.start
        assert charger != warehouse.goal


def test_movement_cost_range():
    warehouse = generate_warehouse(
        rows=8,
        cols=8,
        min_movement_time=1,
        max_movement_time=5,
        seed=100,
    )

    for cost in warehouse.edge_costs.values():
        assert 1 <= cost <= 5


def test_fixed_start_and_goal():
    warehouse = generate_warehouse(
        rows=6,
        cols=6,
        start=(0, 0),
        goal=(5, 5),
        seed=20,
    )

    assert warehouse.start == (0, 0)
    assert warehouse.goal == (5, 5)


def test_ensure_solution():
    warehouse = generate_warehouse(
        rows=8,
        cols=8,
        obstacle_density=0.20,
        charger_count=3,
        battery_capacity=12,
        initial_battery=12,
        start=(0, 0),
        goal=(7, 7),
        seed=42,
        ensure_solution=True,
    )

    assert has_battery_feasible_route(warehouse)


if __name__ == "__main__":
    test_generator_dimensions()
    test_generator_seed_is_reproducible()
    test_start_and_goal_are_open()
    test_exact_charger_count()
    test_chargers_are_open()
    test_movement_cost_range()
    test_fixed_start_and_goal()
    test_ensure_solution()

    print("All warehouse generator tests passed.")