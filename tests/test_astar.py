from maps.test_maps import (
    small_test_map,
    charging_required_map,
)

from warehouse.generator import generate_warehouse

from search.ucs import uniform_cost_search
from search.astar import a_star_search


def test_basic_astar():
    warehouse = small_test_map()

    result = a_star_search(warehouse)

    assert result["success"] is True
    assert result["total_cost"] == 7

    assert (
        result["path"][0].position
        == warehouse.start
    )

    assert (
        result["path"][-1].position
        == warehouse.goal
    )


def test_astar_requires_charging():
    warehouse = charging_required_map()

    result = a_star_search(warehouse)

    assert result["success"] is True
    assert result["total_cost"] == 9

    recharge_actions = [
        action
        for action in result["actions"]
        if action.startswith("Recharge")
    ]

    assert len(recharge_actions) == 1


def test_astar_matches_ucs_optimal_cost():
    for seed in range(5):
        warehouse = generate_warehouse(
            rows=6,
            cols=6,
            obstacle_density=0.15,
            charger_count=2,
            battery_capacity=10,
            initial_battery=10,
            start=(0, 0),
            goal=(5, 5),
            min_movement_time=1,
            max_movement_time=5,
            seed=seed,
            ensure_solution=True,
        )

        ucs_result = uniform_cost_search(
            warehouse
        )

        astar_result = a_star_search(
            warehouse
        )

        assert ucs_result["success"] is True
        assert astar_result["success"] is True

        assert (
            astar_result["total_cost"]
            == ucs_result["total_cost"]
        )


if __name__ == "__main__":
    test_basic_astar()
    test_astar_requires_charging()
    test_astar_matches_ucs_optimal_cost()

    print("All A* tests passed.")