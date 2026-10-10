from maps.test_maps import (
    small_test_map,
    charging_required_map,
)

from search.greedy import greedy_best_first_search


def test_basic_greedy():
    warehouse = small_test_map()
    result = greedy_best_first_search(warehouse)

    assert result["success"] is True
    assert result["total_cost"] is not None
    assert result["path"][0].position == warehouse.start
    assert result["path"][-1].position == warehouse.goal


def test_greedy_with_charging():
    warehouse = charging_required_map()
    result = greedy_best_first_search(warehouse)

    assert result["success"] is True

    recharge_actions = [
        action
        for action in result["actions"]
        if action.startswith("Recharge")
    ]

    assert len(recharge_actions) >= 1


if __name__ == "__main__":
    test_basic_greedy()
    test_greedy_with_charging()

    print("All Greedy tests passed.")