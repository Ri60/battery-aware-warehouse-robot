from warehouse.generator import generate_warehouse

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
        print(
            "Nodes expanded:",
            result["nodes_expanded"],
        )
        return

    print(
        "Total cost:",
        result["total_cost"],
    )

    print(
        "Nodes expanded:",
        result["nodes_expanded"],
    )

    print("\nActions:")

    for action in result["actions"]:
        print("-", action)


def main():
    # Seed makes this warehouse reproducible.
    warehouse = generate_warehouse(
        rows=8,
        cols=8,
        obstacle_density=0.15,
        charger_count=3,
        battery_capacity=12,
        initial_battery=12,
        min_movement_time=1,
        max_movement_time=5,
        seed=42,
        start=(0, 0),
        goal=(7, 7),
    )

    print("\nBattery-Aware Warehouse Delivery Robot")
    print("=" * 55)

    print(
        "Grid size:",
        warehouse.rows,
        "x",
        warehouse.cols,
    )

    print(
        "Start:",
        warehouse.start,
    )

    print(
        "Goal:",
        warehouse.goal,
    )

    print(
        "Battery capacity:",
        warehouse.battery_capacity,
    )

    print(
        "Initial battery:",
        warehouse.initial_battery,
    )

    print(
        "Chargers:",
        warehouse.chargers,
    )

    print(
        "Blocked cells:",
        len(warehouse.blocked_cells),
    )

    display_warehouse(
        warehouse
    )

    # Run all three algorithms on the exact same instance.
    ucs_result = uniform_cost_search(
        warehouse
    )

    greedy_result = greedy_best_first_search(
        warehouse
    )

    astar_result = a_star_search(
        warehouse
    )

    print_result(
        "Uniform Cost Search",
        ucs_result,
    )

    if ucs_result["success"]:
        display_warehouse(
            warehouse,
            ucs_result["path"],
        )

    print_result(
        "Greedy Best-First Search",
        greedy_result,
    )

    if greedy_result["success"]:
        display_warehouse(
            warehouse,
            greedy_result["path"],
        )

    print_result(
        "A* Search",
        astar_result,
    )

    if astar_result["success"]:
        display_warehouse(
            warehouse,
            astar_result["path"],
        )

    results = {
        "UCS": ucs_result,
        "Greedy Best-First": greedy_result,
        "A*": astar_result,
    }

    display_summary(
        results
    )


if __name__ == "__main__":
    main()