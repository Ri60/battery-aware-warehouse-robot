from maps.test_maps import (
    small_test_map,
    charging_required_map,
)

from search.astar import a_star_search


def test_basic_astar():
    warehouse = small_test_map()
    result = a_star_search(warehouse)

    assert result["success"] is True
    assert result["total_cost"] == 7
    assert result["path"][0].position == warehouse.start
    assert result["path"][-1].position == warehouse.goal


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


if __name__ == "__main__":
    test_basic_astar()
    test_astar_requires_charging()

    print("All A* tests passed.")