from maps.test_maps import charging_required_map

from search.ucs import uniform_cost_search
from search.greedy import greedy_best_first_search
from search.astar import a_star_search

from visualization.display import (
    display_warehouse,
    display_summary,
)


def print_result(name, result):
    print("\n" + "=" * 55)
    print(name)
    print("=" * 55)

    if not result["success"]:
        print("No feasible route found.")
        return

    print("Total cost:", result["total_cost"])
    print("Nodes expanded:", result["nodes_expanded"])

    print("\nActions:")

    for action in result["actions"]:
        print("-", action)


def main():
    warehouse = charging_required_map()

    print("\nBattery-Aware Warehouse Delivery Robot")
    print("=" * 55)

    print("Grid size:", warehouse.rows, "x", warehouse.cols)
    print("Start:", warehouse.start)
    print("Goal:", warehouse.goal)
    print("Battery capacity:", warehouse.battery_capacity)
    print("Initial battery:", warehouse.initial_battery)
    print("Chargers:", warehouse.chargers)

    # Show warehouse before searching.
    display_warehouse(warehouse)

    # Run algorithms.
    ucs_result = uniform_cost_search(warehouse)

    greedy_result = greedy_best_first_search(
        warehouse
    )

    astar_result = a_star_search(
        warehouse
    )

    # Individual results.
    print_result(
        "Uniform Cost Search",
        ucs_result,
    )

    display_warehouse(
        warehouse,
        ucs_result["path"],
    )

    print_result(
        "Greedy Best-First Search",
        greedy_result,
    )

    display_warehouse(
        warehouse,
        greedy_result["path"],
    )

    print_result(
        "A* Search",
        astar_result,
    )

    display_warehouse(
        warehouse,
        astar_result["path"],
    )

    # Final comparison.
    results = {
        "UCS": ucs_result,
        "Greedy Best-First": greedy_result,
        "A*": astar_result,
    }

    display_summary(results)


if __name__ == "__main__":
    main()