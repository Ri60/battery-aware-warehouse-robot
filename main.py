from maps.test_maps import charging_required_map
from search.ucs import uniform_cost_search


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

    print("\nRunning Uniform Cost Search...\n")

    result = uniform_cost_search(warehouse)

    if not result["success"]:
        print("No feasible route found.")
        return

    print("Route found!")
    print("Total cost:", result["total_cost"])
    print("Nodes expanded:", result["nodes_expanded"])

    print("\nStates in path:")
    for state in result["path"]:
        print(state)

    print("\nActions:")
    for action in result["actions"]:
        print("-", action)


if __name__ == "__main__":
    main()