import csv
import os
from time import perf_counter

from warehouse.generator import generate_warehouse
from warehouse.grid import Warehouse

from search.ucs import uniform_cost_search
from search.greedy import greedy_best_first_search
from search.astar import a_star_search


ALGORITHMS = [
    ("UCS", uniform_cost_search),
    ("Greedy Best-First", greedy_best_first_search),
    ("A*", a_star_search),
]


TARGET_DISTANCES = [
    3,
    7,
    11,
    14,
]


def get_open_cells_at_distance(
    warehouse,
    distance,
):
    """
    Return open cells whose Manhattan distance
    from the start equals the requested value.
    """

    start_row, start_col = warehouse.start

    candidates = []

    for row in range(warehouse.rows):
        for col in range(warehouse.cols):
            position = (row, col)

            if position == warehouse.start:
                continue

            if position in warehouse.blocked_cells:
                continue

            manhattan_distance = (
                abs(row - start_row)
                + abs(col - start_col)
            )

            if manhattan_distance == distance:
                candidates.append(position)

    return sorted(candidates)


def create_distance_warehouse(
    base_warehouse,
    goal,
):
    """
    Create a warehouse with exactly the same:
    - obstacles
    - chargers
    - edge costs
    - battery settings

    Only the goal changes.
    """

    return Warehouse(
        rows=base_warehouse.rows,
        cols=base_warehouse.cols,
        start=base_warehouse.start,
        goal=goal,
        blocked_cells=base_warehouse.blocked_cells,
        chargers=base_warehouse.chargers,
        edge_costs=base_warehouse.edge_costs,
        battery_capacity=base_warehouse.battery_capacity,
        initial_battery=base_warehouse.initial_battery,
    )


def generate_valid_base_map(
    seed,
):
    """
    Generate one base map containing at least one
    open goal candidate at every target distance.

    The same base map is reused for all distance
    conditions for this seed.
    """

    max_attempts = 100

    for attempt in range(max_attempts):
        adjusted_seed = (
            seed * 1000
            + attempt
        )

        base_warehouse = generate_warehouse(
            rows=8,
            cols=8,
            obstacle_density=0.15,
            charger_count=3,
            battery_capacity=12,
            initial_battery=12,
            min_movement_time=1,
            max_movement_time=5,
            seed=adjusted_seed,
            start=(0, 0),
            goal=(7, 7),
            ensure_solution=False,
        )

        all_distances_available = True

        for distance in TARGET_DISTANCES:
            candidates = get_open_cells_at_distance(
                base_warehouse,
                distance,
            )

            if not candidates:
                all_distances_available = False
                break

        if all_distances_available:
            return base_warehouse

    raise RuntimeError(
        "Could not generate a suitable base map "
        "for the distance experiment."
    )


def run_distance_experiment(
    number_of_seeds=20,
    output_file="results/start_goal_distance_results.csv",
):
    results = []

    print("\nSTART-TO-GOAL DISTANCE EXPERIMENT")
    print("=" * 70)

    for seed in range(number_of_seeds):
        base_warehouse = generate_valid_base_map(
            seed
        )

        for distance in TARGET_DISTANCES:
            candidates = get_open_cells_at_distance(
                base_warehouse,
                distance,
            )

            # Deterministic goal selection.
            goal = candidates[0]

            warehouse = create_distance_warehouse(
                base_warehouse,
                goal,
            )

            print(
                f"Seed {seed + 1}/{number_of_seeds} "
                f"| distance = {distance}",
                end="\r",
            )

            for algorithm_name, search_function in ALGORITHMS:

                start_time = perf_counter()

                result = search_function(
                    warehouse
                )

                end_time = perf_counter()

                execution_time_ms = (
                    end_time - start_time
                ) * 1000

                results.append(
                    {
                        "seed": seed,
                        "distance": distance,
                        "goal": str(goal),
                        "algorithm": algorithm_name,
                        "success": result["success"],
                        "total_cost": result["total_cost"],
                        "nodes_expanded": result["nodes_expanded"],
                        "execution_time_ms": execution_time_ms,
                    }
                )

    print()

    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True,
    )

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "seed",
                "distance",
                "goal",
                "algorithm",
                "success",
                "total_cost",
                "nodes_expanded",
                "execution_time_ms",
            ],
        )

        writer.writeheader()
        writer.writerows(results)

    print_summary(
        results
    )

    print(
        "\nResults saved to:",
        output_file,
    )


def print_summary(results):
    print("\nSUMMARY")
    print("=" * 75)

    for distance in TARGET_DISTANCES:

        print(
            f"\nManhattan distance = {distance}"
        )

        print(
            "-" * 40
        )

        for algorithm_name, _ in ALGORITHMS:

            matching = [
                result
                for result in results
                if result["distance"] == distance
                and result["algorithm"] == algorithm_name
            ]

            successful = [
                result
                for result in matching
                if result["success"]
            ]

            success_count = len(
                successful
            )

            total_count = len(
                matching
            )

            print(
                f"\n{algorithm_name}"
            )

            print(
                "Success:",
                f"{success_count}/{total_count}",
            )

            if not successful:
                continue

            average_cost = sum(
                result["total_cost"]
                for result in successful
            ) / success_count

            average_nodes = sum(
                result["nodes_expanded"]
                for result in successful
            ) / success_count

            average_time = sum(
                result["execution_time_ms"]
                for result in successful
            ) / success_count

            print(
                f"Average cost: "
                f"{average_cost:.2f}"
            )

            print(
                f"Average nodes: "
                f"{average_nodes:.2f}"
            )

            print(
                f"Average runtime: "
                f"{average_time:.4f} ms"
            )


if __name__ == "__main__":
    run_distance_experiment()