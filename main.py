from maps.test_maps import charging_required_map

from search.ucs import uniform_cost_search
from search.greedy import greedy_best_first_search
from search.astar import a_star_search


def print_result(name, result):
    print("\n" + "=" * 55)
    print(name)
    print("=" * 55)

    if not result["success"]:
        print("No feasible route found.")
        return

    print("Total cost:", result["total_cost"])
    print("Nodes expanded:", result["nodes_expanded"])

    print("\nStates in path:")
    for state in result["path"]:
        print(state)

    print("\nActions:")
    for action in result["actions"]:
        print("-", action)


def main():
    warehouse = charging_required_map()

    print("Battery-Aware Warehouse Robot")
    print("-----------------------------")

    print("Grid size:", warehouse.rows, "x", warehouse.cols)
    print("Start:", warehouse.start)
    print("Goal:", warehouse.goal)
    print("Battery capacity:", warehouse.battery_capacity)
    print("Initial battery:", warehouse.initial_battery)
    print("Chargers:", warehouse.chargers)
    print("Blocked cells:", warehouse.blocked_cells)

    ucs_result = uniform_cost_search(warehouse)
    greedy_result = greedy_best_first_search(warehouse)
    astar_result = a_star_search(warehouse)

    print_result(
        "Uniform Cost Search",
        ucs_result,
    )

    print_result(
        "Greedy Best-First Search",
        greedy_result,
    )

    print_result(
        "A* Search",
        astar_result,
    )

    print("\n" + "=" * 55)
    print("SUMMARY")
    print("=" * 55)

    print(
        "UCS:",
        "cost =", ucs_result["total_cost"],
        "| nodes =", ucs_result["nodes_expanded"],
    )

    print(
        "Greedy:",
        "cost =", greedy_result["total_cost"],
        "| nodes =", greedy_result["nodes_expanded"],
    )

    print(
        "A*:",
        "cost =", astar_result["total_cost"],
        "| nodes =", astar_result["nodes_expanded"],
    )


if __name__ == "__main__":
    main()