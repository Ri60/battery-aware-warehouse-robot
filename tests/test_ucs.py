from maps.test_maps import (
    small_test_map,
    charging_required_map,
)

from search.ucs import uniform_cost_search


def test_basic_ucs():
    warehouse = small_test_map()
    result = uniform_cost_search(warehouse)

    assert result["success"] is True
    assert result["total_cost"] == 7
    assert result["path"][0].position == warehouse.start
    assert result["path"][-1].position == warehouse.goal


def test_ucs_requires_charging():
    warehouse = charging_required_map()
    result = uniform_cost_search(warehouse)

    assert result["success"] is True
    assert result["total_cost"] == 9

    recharge_actions = [
        action
        for action in result["actions"]
        if action.startswith("Recharge")
    ]

    assert len(recharge_actions) == 1


if __name__ == "__main__":
    test_basic_ucs()
    test_ucs_requires_charging()

    print("All UCS tests passed.")