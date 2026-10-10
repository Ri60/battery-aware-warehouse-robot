import csv
import os

from warehouse.generator import generate_warehouse

from search.ucs import uniform_cost_search
from search.greedy import greedy_best_first_search
from search.astar import a_star_search

from experiments.metrics import measure_algorithm


ALGORITHMS = [
    (
        "UCS",
        uniform_cost_search,
    ),
    (
        "Greedy Best-First",
        greedy_best_first_search,
    ),
    (
        "A*",
        a_star_search,
    ),
]


def run_single_instance(
    seed,
    rows=8,
    cols=8,
    obstacle_density=0.15,
    charger_count=3,
    battery_capacity=12,
    initial_battery=12,
    min_movement_time=1,
    max_movement_time=5,
    ensure_solution=True,
):
    """
    Generate one warehouse and run all algorithms
    on exactly the same instance.
    """

    warehouse = generate_warehouse(
        rows=rows,
        cols=cols,
        obstacle_density=obstacle_density,
        charger_count=charger_count,
        battery_capacity=battery_capacity,
        initial_battery=initial_battery,
        min_movement_time=min_movement_time,
        max_movement_time=max_movement_time,
        seed=seed,
        start=(0, 0),
        goal=(rows - 1, cols - 1),
        ensure_solution=ensure_solution,
    )

    results = []

    for algorithm_name, search_function in ALGORITHMS:
        measurement = measure_algorithm(
            algorithm_name,
            search_function,
            warehouse,
        )

        results.append(
            measurement
        )

    # UCS is our optimal-cost baseline.
    ucs_result = next(
        result
        for result in results
        if result["algorithm"] == "UCS"
    )

    ucs_cost = (
        ucs_result["total_cost"]
        if ucs_result["success"]
        else None
    )

    rows_for_csv = []

    for result in results:
        if (
            result["success"]
            and ucs_cost is not None
            and ucs_cost > 0
        ):
            suboptimality_ratio = (
                result["total_cost"]
                / ucs_cost
            )
        else:
            suboptimality_ratio = None

        rows_for_csv.append(
            {
                "seed": seed,
                "algorithm": result["algorithm"],
                "rows": rows,
                "cols": cols,
                "obstacle_density": obstacle_density,
                "charger_count": charger_count,
                "battery_capacity": battery_capacity,
                "initial_battery": initial_battery,
                "min_movement_time": min_movement_time,
                "max_movement_time": max_movement_time,
                "success": result["success"],
                "total_cost": result["total_cost"],
                "nodes_expanded": result["nodes_expanded"],
                "execution_time_ms": result[
                    "execution_time_ms"
                ],
                "charging_stops": result[
                    "charging_stops"
                ],
                "moves": result["moves"],
                "suboptimality_ratio": suboptimality_ratio,
            }
        )

    return rows_for_csv


def write_results_to_csv(
    results,
    output_file,
):
    """
    Write experimental results to a CSV file.
    """

    output_directory = os.path.dirname(
        output_file
    )

    if output_directory:
        os.makedirs(
            output_directory,
            exist_ok=True,
        )

    fieldnames = [
        "seed",
        "algorithm",
        "rows",
        "cols",
        "obstacle_density",
        "charger_count",
        "battery_capacity",
        "initial_battery",
        "min_movement_time",
        "max_movement_time",
        "success",
        "total_cost",
        "nodes_expanded",
        "execution_time_ms",
        "charging_stops",
        "moves",
        "suboptimality_ratio",
    ]

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(results)


def print_experiment_summary(results):
    """
    Print average metrics for each algorithm.
    """

    print("\nEXPERIMENT SUMMARY")
    print("=" * 80)

    for algorithm_name, _ in ALGORITHMS:

        algorithm_results = [
            result
            for result in results
            if result["algorithm"] == algorithm_name
        ]

        successful_results = [
            result
            for result in algorithm_results
            if result["success"]
        ]

        total_runs = len(
            algorithm_results
        )

        successful_runs = len(
            successful_results
        )

        print(
            f"\n{algorithm_name}"
        )

        print(
            "-" * len(algorithm_name)
        )

        print(
            "Successful runs:",
            f"{successful_runs}/{total_runs}",
        )

        if not successful_results:
            print(
                "No successful solutions."
            )
            continue

        average_cost = sum(
            result["total_cost"]
            for result in successful_results
        ) / successful_runs

        average_nodes = sum(
            result["nodes_expanded"]
            for result in successful_results
        ) / successful_runs

        average_time = sum(
            result["execution_time_ms"]
            for result in successful_results
        ) / successful_runs

        average_charging_stops = sum(
            result["charging_stops"]
            for result in successful_results
        ) / successful_runs

        average_suboptimality = sum(
            result["suboptimality_ratio"]
            for result in successful_results
            if result["suboptimality_ratio"] is not None
        ) / successful_runs

        print(
            f"Average cost: "
            f"{average_cost:.2f}"
        )

        print(
            f"Average nodes expanded: "
            f"{average_nodes:.2f}"
        )

        print(
            f"Average execution time: "
            f"{average_time:.4f} ms"
        )

        print(
            f"Average charging stops: "
            f"{average_charging_stops:.2f}"
        )

        print(
            f"Average suboptimality ratio: "
            f"{average_suboptimality:.3f}"
        )


def run_experiment(
    number_of_seeds=20,
    rows=8,
    cols=8,
    obstacle_density=0.15,
    charger_count=3,
    battery_capacity=12,
    initial_battery=12,
    min_movement_time=1,
    max_movement_time=5,
    ensure_solution=True,
    output_file="results/baseline_results.csv",
):
    """
    Run a controlled multi-seed experiment.
    """

    all_results = []

    print(
        "\nRunning experiment..."
    )

    print(
        "Seeds:",
        number_of_seeds,
    )

    for seed in range(
        number_of_seeds
    ):
        print(
            f"Running seed "
            f"{seed + 1}/{number_of_seeds}",
            end="\r",
        )

        seed_results = run_single_instance(
            seed=seed,
            rows=rows,
            cols=cols,
            obstacle_density=obstacle_density,
            charger_count=charger_count,
            battery_capacity=battery_capacity,
            initial_battery=initial_battery,
            min_movement_time=min_movement_time,
            max_movement_time=max_movement_time,
            ensure_solution=ensure_solution,
        )

        all_results.extend(
            seed_results
        )

    print()

    write_results_to_csv(
        all_results,
        output_file,
    )

    print_experiment_summary(
        all_results
    )

    print(
        "\nResults saved to:",
        output_file,
    )

    return all_results


if __name__ == "__main__":
    run_experiment()