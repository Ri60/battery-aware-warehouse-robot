from experiments.runner import (
    run_single_instance,
)


def test_all_algorithms_use_same_instance():
    results = run_single_instance(
        seed=42,
        rows=6,
        cols=6,
        obstacle_density=0.10,
        charger_count=2,
        battery_capacity=10,
        initial_battery=10,
        ensure_solution=True,
    )

    assert len(results) == 3

    algorithms = {
        result["algorithm"]
        for result in results
    }

    assert algorithms == {
        "UCS",
        "Greedy Best-First",
        "A*",
    }


def test_ucs_and_astar_match_cost():
    results = run_single_instance(
        seed=42,
        rows=6,
        cols=6,
        obstacle_density=0.10,
        charger_count=2,
        battery_capacity=10,
        initial_battery=10,
        ensure_solution=True,
    )

    result_by_algorithm = {
        result["algorithm"]: result
        for result in results
    }

    ucs = result_by_algorithm["UCS"]
    astar = result_by_algorithm["A*"]

    assert ucs["success"] is True
    assert astar["success"] is True

    assert (
        ucs["total_cost"]
        == astar["total_cost"]
    )


def test_suboptimality_ratio():
    results = run_single_instance(
        seed=42,
        rows=6,
        cols=6,
        obstacle_density=0.10,
        charger_count=2,
        battery_capacity=10,
        initial_battery=10,
        ensure_solution=True,
    )

    result_by_algorithm = {
        result["algorithm"]: result
        for result in results
    }

    assert (
        result_by_algorithm["UCS"][
            "suboptimality_ratio"
        ]
        == 1.0
    )

    assert (
        result_by_algorithm["A*"][
            "suboptimality_ratio"
        ]
        == 1.0
    )


if __name__ == "__main__":
    test_all_algorithms_use_same_instance()
    test_ucs_and_astar_match_cost()
    test_suboptimality_ratio()

    print(
        "All experiment tests passed."
    )