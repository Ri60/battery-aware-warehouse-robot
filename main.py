from warehouse.generator import generate_warehouse

from maps.test_maps import (
    small_test_map,
    charging_required_map,
)

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
        print("Nodes expanded:", result["nodes_expanded"])
        return

    print("Total cost:", result["total_cost"])
    print("Nodes expanded:", result["nodes_expanded"])

    print("\nActions:")

    for action in result["actions"]:
        print("-", action)


def get_integer(prompt, default=None, minimum=None):
    while True:
        value = input(prompt).strip()

        if value == "" and default is not None:
            return default

        try:
            value = int(value)

            if minimum is not None and value < minimum:
                print(f"Please enter a value of at least {minimum}.")
                continue

            return value

        except ValueError:
            print("Please enter a whole number.")


def get_float(prompt, default=None, minimum=None, maximum=None):
    while True:
        value = input(prompt).strip()

        if value == "" and default is not None:
            return default

        try:
            value = float(value)

            if minimum is not None and value < minimum:
                print(f"Value must be at least {minimum}.")
                continue

            if maximum is not None and value > maximum:
                print(f"Value must be at most {maximum}.")
                continue

            return value

        except ValueError:
            print("Please enter a number.")


def get_position(name, rows, cols):
    while True:
        print(
            f"\n{name}: enter row and column, "
            "or press Enter to randomize."
        )

        value = input(
            f"{name} (example: 2,3): "
        ).strip()

        if value == "":
            return None

        try:
            row_text, col_text = value.split(",")

            row = int(row_text.strip())
            col = int(col_text.strip())

            if not (0 <= row < rows and 0 <= col < cols):
                print(
                    f"Position must be inside a "
                    f"{rows} x {cols} warehouse."
                )
                continue

            return (row, col)

        except (ValueError, TypeError):
            print(
                "Use row,column format, for example 2,3."
            )


def choose_warehouse():
    print("\nChoose an environment/map:")
    print("1 - Random/generated warehouse")
    print("2 - Small known test map")
    print("3 - Charging-required test map")

    while True:
        choice = input("Map choice [1]: ").strip() or "1"

        if choice == "1":
            rows = get_integer(
                "Rows [8]: ",
                default=8,
                minimum=2,
            )

            cols = get_integer(
                "Columns [8]: ",
                default=8,
                minimum=2,
            )

            obstacle_density = get_float(
                "Obstacle density 0-0.9 [0.15]: ",
                default=0.15,
                minimum=0.0,
                maximum=0.9,
            )

            charger_count = get_integer(
                "Number of chargers [3]: ",
                default=3,
                minimum=0,
            )

            battery_capacity = get_integer(
                "Battery capacity [12]: ",
                default=12,
                minimum=1,
            )

            initial_battery = get_integer(
                f"Initial battery [{battery_capacity}]: ",
                default=battery_capacity,
                minimum=0,
            )

            if initial_battery > battery_capacity:
                print(
                    "Initial battery cannot exceed capacity. "
                    "Using full capacity instead."
                )
                initial_battery = battery_capacity

            seed_text = input(
                "Random seed [42, type random for random seed]: "
            ).strip()

            if seed_text.lower() == "random":
                seed = None
            elif seed_text == "":
                seed = 42
            else:
                try:
                    seed = int(seed_text)
                except ValueError:
                    print("Invalid seed. Using 42.")
                    seed = 42

            start = get_position(
                "Start",
                rows,
                cols,
            )

            goal = get_position(
                "Goal",
                rows,
                cols,
            )

            if (
                start is not None
                and goal is not None
                and start == goal
            ):
                print(
                    "Start and goal cannot be the same. "
                    "Goal will be randomized."
                )
                goal = None

            return generate_warehouse(
                rows=rows,
                cols=cols,
                obstacle_density=obstacle_density,
                charger_count=charger_count,
                battery_capacity=battery_capacity,
                initial_battery=initial_battery,
                min_movement_time=1,
                max_movement_time=5,
                seed=seed,
                start=start,
                goal=goal,
                ensure_solution=True,
                max_attempts=500,
            )

        if choice == "2":
            return small_test_map()

        if choice == "3":
            return charging_required_map()

        print("Please choose 1, 2, or 3.")


def choose_algorithm():
    print("\nChoose a search algorithm:")
    print("1 - Uniform Cost Search")
    print("2 - Greedy Best-First Search")
    print("3 - A* Search")
    print("4 - Compare all three")

    while True:
        choice = input("Algorithm choice [4]: ").strip() or "4"

        if choice in {"1", "2", "3", "4"}:
            return choice

        print("Please choose 1, 2, 3, or 4.")


def run_algorithm(name, algorithm, warehouse):
    result = algorithm(warehouse)

    print_result(
        name,
        result,
    )

    if result["success"]:
        print("\nRoute:")
        display_warehouse(
            warehouse,
            result["path"],
        )

    return result


def main():
    print("\nBattery-Aware Warehouse Delivery Robot")
    print("=" * 55)

    warehouse = choose_warehouse()

    print("\nSelected Warehouse")
    print("=" * 55)

    print(
        "Grid size:",
        warehouse.rows,
        "x",
        warehouse.cols,
    )

    print("Start:", warehouse.start)
    print("Goal:", warehouse.goal)
    print(
        "Battery capacity:",
        warehouse.battery_capacity,
    )
    print(
        "Initial battery:",
        warehouse.initial_battery,
    )
    print("Chargers:", warehouse.chargers)
    print(
        "Blocked cells:",
        len(warehouse.blocked_cells),
    )

    print("\nWarehouse:")
    display_warehouse(warehouse)

    algorithm_choice = choose_algorithm()

    results = {}

    if algorithm_choice in {"1", "4"}:
        results["UCS"] = run_algorithm(
            "Uniform Cost Search",
            uniform_cost_search,
            warehouse,
        )

    if algorithm_choice in {"2", "4"}:
        results["Greedy Best-First"] = run_algorithm(
            "Greedy Best-First Search",
            greedy_best_first_search,
            warehouse,
        )

    if algorithm_choice in {"3", "4"}:
        results["A*"] = run_algorithm(
            "A* Search",
            a_star_search,
            warehouse,
        )

    if len(results) > 1:
        print("\nAlgorithm Comparison")
        display_summary(results)


if __name__ == "__main__":
    main()